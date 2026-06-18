"""
Klein 4B inference forward with img2img support for the GPU/gemlite backend.
Drop-in replacement for vendor/image-studio/backend_gpu/diffusion_klein.py

Adds init_image + image_strength params to diffusion_forward for character
consistency via img2img.
"""
from __future__ import annotations

import logging
from typing import Optional

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image

from diffusers import FlowMatchEulerDiscreteScheduler, Flux2Pipeline
from diffusers.pipelines.flux2.pipeline_flux2 import retrieve_timesteps

log = logging.getLogger(__name__)


def _mflux_empirical_mu(image_seq_len: int, num_steps: int) -> float:
    a1, b1 = 8.73809524e-05, 1.89833333
    a2, b2 = 0.00016927, 0.45666666
    if image_seq_len > 4300:
        return float(a2 * image_seq_len + b2)
    m_200 = a2 * image_seq_len + b2
    m_10 = a1 * image_seq_len + b1
    a = (m_200 - m_10) / 190.0
    b = m_200 - 200.0 * a
    return float(a * num_steps + b)


DEFAULT_GUIDANCE = 1.0
DEFAULT_NUM_STEPS = 4
KLEIN_OUTPUT_LAYERS = (9, 18, 27)


@torch.no_grad()
def _encode_klein_qwen3_prompt(
    text_encoder: nn.Module, tokenizer, prompt: str, *, max_sequence_length: int,
) -> torch.Tensor:
    device = text_encoder.device
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True, enable_thinking=False,
    )
    inputs = tokenizer(
        text, return_tensors="pt", padding="max_length", truncation=True,
        max_length=max_sequence_length,
    )
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)
    output = text_encoder(
        input_ids=input_ids, attention_mask=attention_mask,
        output_hidden_states=True, use_cache=False,
    )
    out = torch.stack([output.hidden_states[k] for k in KLEIN_OUTPUT_LAYERS], dim=1)
    batch_size, num_channels, seq_len, hidden_dim = out.shape
    return out.permute(0, 2, 1, 3).reshape(batch_size, seq_len, num_channels * hidden_dim)


def _build_default_scheduler() -> FlowMatchEulerDiscreteScheduler:
    return FlowMatchEulerDiscreteScheduler(
        num_train_timesteps=1000, shift=3.0, use_dynamic_shifting=True,
        base_shift=0.5, max_shift=1.15, base_image_seq_len=256, max_image_seq_len=4096,
    )


@torch.no_grad()
def _encode_init_image_to_latents(
    init_image: Image.Image, vae: nn.Module,
    height: int, width: int,
    transformer_device: torch.device, activation_dtype: torch.dtype,
) -> torch.Tensor:
    """Encode PIL image → VAE → patchify → BN normalize → pack.
    Returns (1, image_seq_len, in_channels) packed latents."""
    from diffusers import Flux2Pipeline

    init_image = init_image.convert("RGB").resize((width, height), Image.LANCZOS)
    img_array = np.array(init_image).astype(np.float32)
    img_array = img_array / 127.5 - 1.0
    img_tensor = torch.from_numpy(img_array).permute(2, 0, 1).unsqueeze(0)
    img_tensor = img_tensor.to(device=vae.device, dtype=torch.bfloat16)

    with torch.no_grad():
        encoded = vae.encode(img_tensor).latent_dist.sample()
        shift_factor = getattr(vae.config, "shift_factor", 0.0)
        scaling_factor = getattr(vae.config, "scaling_factor", 1.0)
        encoded = (encoded - shift_factor) * scaling_factor

    encoded = encoded.to(device=transformer_device, dtype=activation_dtype)

    # Patchify via pixel_unshuffle: (1, 32, H/8, W/8) → (1, 128, H/16, W/16)
    encoded = F.pixel_unshuffle(encoded, 2)

    # BN normalize (undo the denormalize done at decode time)
    bn_mean = vae.bn.running_mean.view(1, -1, 1, 1).to(encoded.device, encoded.dtype)
    bn_var = vae.bn.running_var.view(1, -1, 1, 1).to(encoded.device, encoded.dtype)
    bn_eps = getattr(vae.config, "batch_norm_eps", 1e-6)
    encoded = (encoded - bn_mean) / torch.sqrt(bn_var + bn_eps)

    # Pack: (1, 128, H/16, W/16) → (1, image_seq_len, 128)
    return Flux2Pipeline._pack_latents(encoded)


@torch.no_grad()
def diffusion_forward(
    transformer: nn.Module, text_encoder: nn.Module, tokenizer, vae: nn.Module,
    prompt: str, *, height: int, width: int,
    num_steps: int = DEFAULT_NUM_STEPS, seed: int = 0,
    max_sequence_length: int = 1024, guidance: float = DEFAULT_GUIDANCE,
    scheduler: Optional[FlowMatchEulerDiscreteScheduler] = None,
    init_image: Optional[Image.Image] = None,
    image_strength: float = 0.5,
) -> Image.Image:
    transformer_device = next(transformer.parameters()).device
    vae_device = next(vae.parameters()).device

    if height % 32 != 0 or width % 32 != 0:
        raise ValueError(f"height={height} and width={width} must be multiples of 32.")

    if scheduler is None:
        scheduler = _build_default_scheduler()

    # 1. Text encode
    prompt_embeds = _encode_klein_qwen3_prompt(
        text_encoder=text_encoder, tokenizer=tokenizer,
        prompt=prompt, max_sequence_length=max_sequence_length,
    )
    text_ids = Flux2Pipeline._prepare_text_ids(prompt_embeds).to(transformer_device)
    activation_dtype = getattr(transformer, "_inference_dtype", torch.float16)
    prompt_embeds_t = prompt_embeds.to(device=transformer_device, dtype=activation_dtype)

    # 2. Latent geometry
    vae_scale_factor = 2 ** (len(vae.config.block_out_channels) - 1)
    h_lat = 2 * (int(height) // (vae_scale_factor * 2))
    w_lat = 2 * (int(width) // (vae_scale_factor * 2))
    in_c = transformer.config.in_channels // 4
    noise_4d_shape = (1, in_c * 4, h_lat // 2, w_lat // 2)

    # 3. Schedule
    mu = _mflux_empirical_mu(image_seq_len=(h_lat // 2) * (w_lat // 2), num_steps=num_steps)
    sigmas = np.linspace(1.0, 1.0 / num_steps, num_steps)
    if hasattr(scheduler.config, "use_flow_sigmas") and scheduler.config.use_flow_sigmas:
        sigmas = None
    timesteps, num_steps_eff = retrieve_timesteps(
        scheduler, num_steps, transformer_device, sigmas=sigmas, mu=mu,
    )
    if hasattr(scheduler, "set_begin_index"):
        scheduler.set_begin_index(0)

    # 4. Prepare latents
    gen = torch.Generator(device="cpu").manual_seed(int(seed))

    do_img2img = init_image is not None and 0.0 < image_strength <= 1.0

    if do_img2img:
        # sigma = image_strength (0.35 = 35% noise, 65% init image)
        sigma_val = max(0.15, min(1.0, image_strength))

        # Use more steps so denoising has room to work from sigma
        effective_steps = max(num_steps, 12)
        mu = _mflux_empirical_mu(image_seq_len=(h_lat // 2) * (w_lat // 2), num_steps=effective_steps)
        sigmas = np.linspace(1.0, 1.0 / effective_steps, effective_steps)
        if hasattr(scheduler.config, "use_flow_sigmas") and scheduler.config.use_flow_sigmas:
            sigmas = None
        timesteps, num_steps_eff = retrieve_timesteps(
            scheduler, effective_steps, transformer_device, sigmas=sigmas, mu=mu,
        )

        # Find first timestep where noise level (t/1000) <= sigma
        target_t = sigma_val * 1000.0
        start_step = num_steps_eff - 1
        for i, t in enumerate(timesteps):
            if float(t) / 1000.0 <= target_t:
                start_step = i
                break
        start_step = max(1, min(start_step, num_steps_eff - 2))

        log.info("img2img: strength=%.2f sigma=%.3f start=%d/%d active=%d",
                 image_strength, sigma_val, start_step, num_steps_eff,
                 num_steps_eff - start_step)

        # Generate pure noise (4D) and pack it
        pure_noise_4d = torch.randn(noise_4d_shape, generator=gen, dtype=torch.float32)
        pure_noise_4d = pure_noise_4d.to(device=transformer_device, dtype=activation_dtype)
        pure_noise_packed = Flux2Pipeline._pack_latents(pure_noise_4d)

        # Encode init image → packed latents
        init_packed = _encode_init_image_to_latents(
            init_image, vae, height, width, transformer_device, activation_dtype,
        )

        # Blend in packed space: (1-sigma)*init + sigma*noise
        latents = (1.0 - sigma_val) * init_packed + sigma_val * pure_noise_packed

        # latent_ids from shape info
        latent_ids = Flux2Pipeline._prepare_latent_ids(pure_noise_4d).to(transformer_device)
    else:
        latents_4d = torch.randn(noise_4d_shape, generator=gen, dtype=torch.float32)
        latents_4d = latents_4d.to(device=transformer_device, dtype=activation_dtype)
        latent_ids = Flux2Pipeline._prepare_latent_ids(latents_4d).to(transformer_device)
        latents = Flux2Pipeline._pack_latents(latents_4d)
        start_step = 0

    image_seq_len = latents.shape[1]
    guidance_t = torch.full([1], guidance, device=transformer_device, dtype=torch.float32)
    guidance_t = guidance_t.expand(latents.shape[0])

    # 5. Denoising loop
    for i, t in enumerate(timesteps):
        if i < start_step:
            continue
        timestep = t.expand(latents.shape[0]).to(latents.dtype)
        noise_pred = transformer(
            hidden_states=latents,
            timestep=timestep / 1000,
            guidance=guidance_t,
            encoder_hidden_states=prompt_embeds_t,
            txt_ids=text_ids,
            img_ids=latent_ids,
            return_dict=False,
        )[0]
        latent_dtype = latents.dtype
        latents = scheduler.step(noise_pred, t, latents, return_dict=False)[0]
        if latents.dtype != latent_dtype:
            latents = latents.to(latent_dtype)

    # 6. Unpack → VAE decode
    latents = Flux2Pipeline._unpack_latents_with_ids(latents, latent_ids)
    latents = latents.to(device=vae_device, dtype=torch.bfloat16)

    bn_mean = vae.bn.running_mean.view(1, -1, 1, 1).to(latents.device, latents.dtype)
    bn_std = torch.sqrt(
        vae.bn.running_var.view(1, -1, 1, 1) + vae.config.batch_norm_eps
    ).to(latents.device, latents.dtype)
    latents = latents * bn_std + bn_mean
    latents = Flux2Pipeline._unpatchify_latents(latents)

    image = vae.decode(latents, return_dict=False)[0]
    img = image[0].clamp(-1.0, 1.0).float()
    img = (img + 1.0) * 127.5
    img = img.clamp(0.0, 255.0).round().to(torch.uint8)
    img = img.permute(1, 2, 0).cpu().numpy()
    return Image.fromarray(img, mode="RGB")


__all__ = ["diffusion_forward", "DEFAULT_GUIDANCE", "DEFAULT_NUM_STEPS"]

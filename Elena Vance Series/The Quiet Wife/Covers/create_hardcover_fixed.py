from PIL import Image
from fpdf import FPDF
import os

covers_dir = r'D:\Kapil\Books\The Quiet Wife\covers'

def create_hardcover_cover(back_path, spine_path, front_path, output_path, page_count=156):
    """Create KDP hardcover template.
    
    Source images are at ~120 DPI and represent the full cover with extra height.
    We scale them to 300 DPI based on their print width, then crop to trim height.
    """
    
    trim_w = 5.5
    trim_h = 8.5
    bleed = 0.125
    DPI = 300
    
    spine_in = 0.0025 * page_count + 0.059  # 0.449"
    
    cover_w_in = 14.115
    cover_h_in = 10.417
    
    content_h = trim_h + 2 * bleed  # 8.75"
    content_offset = (cover_h_in - content_h) / 2  # 0.8335"
    
    canvas_w = int(cover_w_in * DPI)  # 4234
    canvas_h = int(cover_h_in * DPI)  # 3125
    
    canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))
    
    # X positions in pixels
    back_flap_w = (cover_w_in - (trim_w + bleed) - spine_in - (trim_w + bleed)) / 2
    back_panel_x = int(back_flap_w * DPI)
    spine_panel_x = int((back_flap_w + trim_w + bleed) * DPI)
    front_panel_x = int((back_flap_w + trim_w + bleed + spine_in) * DPI)
    content_y = int(content_offset * DPI)
    
    # Panel dimensions at 300 DPI
    panel_w_px = int((trim_w + bleed) * DPI)  # 1688
    spine_w_px = int(spine_in * DPI)  # 135
    content_h_px = int(content_h * DPI)  # 2625
    
    print(f"Canvas: {canvas_w}x{canvas_h}")
    print(f"Panel targets: back={panel_w_px}x{content_h_px}, spine={spine_w_px}x{content_h_px}, front={panel_w_px}x{content_h_px}")
    
    def place_panel(img, panel_x, target_w, target_h):
        """Scale image so its width matches the panel width at 300 DPI.
        The source is at ~120 DPI, so scale factor = 300/120 = 2.5.
        Then crop height to target_h (center crop)."""
        src_w, src_h = img.size
        
        # Scale to target width
        scale = target_w / src_w
        new_w = target_w
        new_h = int(src_h * scale)
        
        resized = img.resize((new_w, new_h), Image.LANCZOS)
        
        # Crop height to target_h (center crop to keep the main cover area)
        if new_h > target_h:
            top = (new_h - target_h) // 2
            resized = resized.crop((0, top, new_w, top + target_h))
        elif new_h < target_h:
            # If still too short, stretch (shouldn't happen with correct source)
            resized = resized.resize((target_w, target_h), Image.LANCZOS)
        
        canvas.paste(resized, (panel_x, content_y))
        print(f"  {img.size} -> {resized.size} at x={panel_x}")
    
    back_img = Image.open(back_path).convert("RGB")
    spine_img = Image.open(spine_path).convert("RGB")
    front_img = Image.open(front_path).convert("RGB")
    
    print(f"\nPlacing panels:")
    place_panel(back_img, back_panel_x, panel_w_px, content_h_px)
    place_panel(spine_img, spine_panel_x, spine_w_px, content_h_px)
    place_panel(front_img, front_panel_x, panel_w_px, content_h_px)
    
    # Save PNG
    png_path = output_path.replace('.pdf', '.png')
    canvas.save(png_path, 'PNG')
    
    # Create PDF
    pdf = FPDF(unit="pt", format=(canvas_w, canvas_h))
    pdf.set_auto_page_break(False)
    pdf.set_margins(0, 0, 0)
    pdf.add_page()
    pdf.image(canvas, x=0, y=0, w=canvas_w, h=canvas_h)
    pdf.output(output_path)
    print(f"\nSaved: {output_path}")

create_hardcover_cover(
    back_path=os.path.join(covers_dir, 'back_cover.png'),
    spine_path=os.path.join(covers_dir, 'spine_cover.png'),
    front_path=os.path.join(covers_dir, 'front_cover.png'),
    output_path=os.path.join(covers_dir, 'hardcover_cover.pdf'),
    page_count=156
)

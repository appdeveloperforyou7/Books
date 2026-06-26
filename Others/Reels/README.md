# Reels Generator

A reusable, project-agnostic tool that turns a **book's Kindle cover** into
**vertical marketing reels & shorts** (Instagram Reels / YouTube Shorts / TikTok
format) — **100% free and fully local** (no API keys, no cloud, no paid models).

## What it produces

For each "hook" in `ReelGen.md` it generates:

- **Image shorts** (`PNG`) — a composed 9:16 frame: blurred cover background,
  the book cover with a brand-colored frame, title, hook text, author, and a
  call-to-action bar.
- **Video reels** (`MP4`) — the same frame animated with a slow **Ken Burns
  zoom** and fade in/out (24fps, `libx264`, no audio).

Brand colors are **auto-extracted from the Kindle cover** (background = darkest
tone, accent = most vibrant tone), so each book's reel matches its own cover.

## How it works (the AI workflow)

1. You point the AI at this folder and say: *"Read `ReelGen.md` and generate
   reels for `<book>`, copy them into `<project folder>`."*
2. The AI edits `ReelGen.md` with the book's details, KDP link, Kindle cover
   filename, hooks, and target project folder(s).
3. The AI drops the Kindle cover image into this folder.
4. The AI runs the generator. Outputs land in `output/` and are copied into each
   `target_projects` folder under a `reels/` subfolder.

## Files

- `ReelGen.md` — the config/spec for the current book (edit per project).
- `generate_reels.py` — the generator (config parse → palette → compose → render → copy).
- `requirements.txt` — minimal local dependencies.
- `output/` — generated assets (created on run) + `_manifest.json`.

## Setup (one time)

```powershell
python -m pip install -r requirements.txt
```

Video output also needs **ffmpeg** on your PATH (moviepy uses it). If you only
want image shorts, Pillow alone is enough.

## Usage

```powershell
# Edit ReelGen.md first (book info + drop the Kindle cover in this folder)
python .\generate_reels.py --config .\ReelGen.md

# Override formats without editing the file
python .\generate_reels.py --formats image
python .\generate_reels.py --formats image,video

# Generate without copying into project folders
python .\generate_reels.py --no-copy
```

## ReelGen.md reference

| Section          | Keys                                                            |
|------------------|-----------------------------------------------------------------|
| `book`           | `title`, `author`, `tagline`, `kdp_link`, `cover_image`, `reference_image` |
| `reel_settings`  | `count`, `formats` (`image,video`), `duration_seconds`, `aspect_ratio` (`9:16`/`1:1`/`16:9`/`4:5`), `resolution` (`480p`/`720p`/`1080p`), `style`, `call_to_action`, `ken_burns` |
| `branding`       | `mode` (`auto` to derive from cover), `font_family`            |
| `video_generation` | `provider`, `preset`, `fade_seconds`, `zoom`                  |
| `hooks`          | `- ...` list of teaser lines; supports `{title}` `{author}` `{tagline}` `{kdp_link}` placeholders |
| `target_projects`| `- ...` list of absolute/relative folders to copy outputs into |

## Reusing across book projects

Because everything is driven by `ReelGen.md`, the **same folder and script work
for every book**. For a new book, the AI just rewrites the config values and
swaps in that book's cover — no code changes needed. To keep a per-book record,
copy the generated `output/` into the book's own `reels/` folder (the script
does this automatically when the folder is listed under `target_projects`).

## Notes

- Reels/Shorts are **vertical** by default (`9:16`). Square (`1:1`) and landscape (`16:9`) are supported too.
- Text is rendered with Pillow (no ImageMagick needed), using Arial by default on Windows.
- No audio is added; add a soundtrack in your editor of choice or extend `generate_video_reel`.

# ReelGen — Book Reel / Short Generator

> Single source of truth for generating marketing reels & shorts for a book.
> The AI reads this file, fills in the values for the current book, then runs
> `python generate_reels.py`. Outputs are written to `output/` and copied into
> each folder listed under `target_projects` (under a `reels/` subfolder).
>
> Format rules:
> - `## section` starts a section.
> - Inside a section, use `key: value` lines.
> - A section made only of `- item` lines is a list (used for `hooks` and
>   `target_projects`).
> - Paths are relative to this folder (absolute paths also work).
> - Lines starting with `#` are notes/comments and are ignored.

## book

title: My Book Title
author: Author Name
tagline: A gripping, emotionally charged story you can't put down
kdp_link: https://www.amazon.com/dp/YOUR_KDP_ASIN
cover_image: kindle_cover.jpg
reference_image: kindle_cover.jpg

## reel_settings

count: 3
formats: image, video
duration_seconds: 15
aspect_ratio: 9:16
resolution: 1080p
style: cinematic
call_to_action: Read it now — link in bio
ken_burns: true

## branding

mode: auto
font_family: arial

## video_generation

provider: moviepy
preset: medium
fade_seconds: 0.4
zoom: 0.07

## hooks

- {title} — the story everyone will be talking about this year.
- One choice. One night. A secret that changes everything.
- If you love {tagline}, this book is your next obsession.

## target_projects

- D:\Kapil\Books\ProjectA
- D:\Kapil\Books\ProjectB

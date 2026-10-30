# SPLY/DMND website

Static website for SPLY/DMND, a DJ management, artist representation, hospitality and event agency.

## How it's organized
- `site/` is the published website. Cloudflare Pages serves this folder as-is.
- `build.py` generates the pages in `site/` from the roster, dates and services lists at the top of the file.
- `site/images/` holds artist photos.

## Making changes
1. Edit the lists in `build.py` (roster, dates, services) or the styles in `site/styles.css`.
2. Run `python3 build.py` to regenerate the pages.
3. Commit and push. Cloudflare Pages publishes the new version automatically.

## Cloudflare Pages settings
- Framework preset: None
- Build command: (leave empty)
- Build output directory: `site`

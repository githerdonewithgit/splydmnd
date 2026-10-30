# SPLY/DMND website

Static website for SPLY/DMND, a DJ management, artist representation, hospitality and event agency.

## How it's organized
- `site/` is the published website. Cloudflare serves this folder as-is.
- `build.py` generates the pages in `site/` from the roster, dates and services lists at the top of the file.
- `site/images/` holds artist photos.

## Making changes
1. Edit the lists in `build.py` (roster, dates, services) or the styles in `site/styles.css`.
2. Run `python3 build.py` to regenerate the pages.
3. Commit and push. Cloudflare publishes the new version automatically.

## Cloudflare
The site is deployed as a Cloudflare Worker with static assets. `wrangler.jsonc` tells Cloudflare to serve the `site` folder. Every push to `main` deploys automatically.

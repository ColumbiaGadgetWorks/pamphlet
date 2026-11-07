# Project summary: Columbia Gadget Works print materials

A record of the work done so far and what someone picking this up next needs
to know. Written November 2026. For how to build and print, see
[README.md](README.md); for the pamphlet content checklist, see
[CONTENT.md](CONTENT.md).

## What this repo makes

| Piece | Source | Print files (in `build/`) |
|---|---|---|
| Tri-fold pamphlet (letter, landscape) | `pamphlet.html` | `pamphlet.pdf` (home/office printer), `pamphlet-vistaprint.pdf` (Vistaprint) |
| Business card (3.5 x 2 in, two-sided) | `business-card.html` | `business-card.pdf` (print shop, 1/8 in bleed), `business-card-vistaprint.pdf` (Vistaprint), `business-card-sheet.pdf` (10-up letter sheet, Avery 8371 layout) |
| Yard sign (24 x 18 in, white coroplast) | `scripts/make_yard_sign.py` | `yard-sign/stencil-rust.svg`, `stencil-dark.svg`, `stencil-one-color.svg` (laser files), `yard-sign.pdf` (sign shop print), `preview.png` |

Everything is rebuilt by `./build.sh` (Python: `pip install -r requirements.txt`;
Node: `npm install` for Playwright). The build writes the QR codes, the yard
sign geometry, then every PDF and preview image with headless Chromium. The
built files are committed so they can be printed without building.

Work happens on `main` in `ColumbiaGadgetWorks/pamphlet` (the user asked for
pushes straight to `main`).

## House rules from the user

These came up during the project and apply to anything new:

- **No em dashes.** Professional, plain, not verbose. No cutesy lines.
- **No AI-generated photos or logos.** Only real shop photos (from the
  website repo, `assets/img/`) and the real gear logo (`static/img/cgw-gear.png`).
  Icons are the official brand marks from Simple Icons (CC0); the website
  also uses Bootstrap Icons (MIT) for generic icons.
- **Design language** copies the CGW website (rust `#BF4D28`, steel
  `#1C2228`, warm paper `#FAF7F2`, Arial, uppercase eyebrow labels, cards with
  a rust left rule, dark photo hero) and the shop kiosk page (drafting-grid
  background, mono labels, ink-bordered title blocks).
- **Leave out:** the phone number, "scout troops", a "teach a class" call to
  action (for now), and the $100 Supporter dues tier.

## Current facts printed on the materials

Check these if anything changes; they appear in more than one place.

- **Open Hack Night:** free, every Thursday, 6 to 8 pm.
- **Free monthly classes:** first **Tuesday** of every month, 6 to 8 pm,
  through October 2027, funded by the City of Columbia Office of Cultural
  Affairs (required credit line: "Financial assistance for this program has
  been provided by the City of Columbia Office of Cultural Affairs").
  **Sign-ups with limited seats** at columbiagadgetworks.org/classes.
- **Address:** 1404 Grand Ave, Columbia, MO 65203. Entrance is the **front
  door with the gear logo**, which has the doorbell (there is no side door).
- **Email:** mail@columbiagadgetworks.org. **Membership:** $50/month.
- **Online:** website columbiagadgetworks.org, wiki wiki.comogadget.casa,
  Discord discord.gg/yjpeBrAjuR (confirmed never expires), and
  columbiagadgetworks.org/links for everything.
- **Socials:** Instagram @columbiagadgetworks, TikTok @columbia.gadget.w,
  Facebook /columbiagadgetworks, Bluesky @comogadgetworks.bsky.social,
  LinkedIn (company page 111805202).
- **Tools highlighted:** laser cutter (80 W CO2), Shapeoko 4 XL CNC router,
  Bambu Lab X1 Carbon and A1 3D printers, Bridgeport mill, Clausing lathe,
  MIG/TIG/stick welding, metal casting, electronics bench, woodshop with a
  SawStop contractor table saw.

## Work log

### Pamphlet
1. Built the tri-fold from the website's content and design, with QR codes
   for Discord, website, wiki, classes and donations, and real equipment photos.
2. Revisions: front door wording; social media with icons and handles (no
   QR codes); removed scout troops, teach-a-class and cutesy Discord copy;
   classes QR pointed at the calendar, then at the sign-up page; standard
   $50 dues only; woodshop card mentioning the SawStop; LinkedIn added;
   phone removed; "Follow our socials" with columbiagadgetworks.org/links;
   Discord described as project talk for makers and hobbyists.
3. Classes updated to the first Tuesday, 6 to 8 pm, with no start date (so it
   doesn't look dated) and "Seats are limited, so sign up to save yours."
4. Vistaprint version (see below), plus a slightly shorter back-panel
   "Getting in" line so the narrower middle panel fits.

### Business card
1. Two-sided card: dark front with the gear logo and name; grid-paper back.
2. Revisions: more info; QR box fitted to the code; larger front; social
   icon row (Instagram, Facebook, TikTok, Bluesky, LinkedIn) with "Follow our
   socials" and the /links address; Discord box says "Projects, makers, and
   hobbyists"; phone removed; tool tags (Mill, Lathe, 3D printers, Laser
   cutter, Table saw, Welding) moved to the front because the back had no room.
3. Vistaprint version, then a taller rust stripe (0.12 in visible after
   trimming) because Vistaprint's safe line made the old stripe look cropped.

### Yard sign
"FREE MAKERSPACE" in rust, the gear logo (rust) beside "COLUMBIA / GADGET /
WORKS" (dark), and COLUMBIAGADGETWORKS.ORG. Set in Big Shoulders Stencil
(SIL OFL, in `assets/fonts/`). The gear is traced from the PNG logo and given
four bridges across its ring. The build fails if any stencil has an island
(a piece that would fall out); currently none. A 24 x 18 in stencil fits the
shop laser's 28 x 20 in bed.

### Website (`ColumbiaGadgetWorks/website`), all merged
- **PR #17:** entrance is the front door; added Instagram and TikTok.
- **PR #19:** added LinkedIn.
- **PR #21:** new `/links` page (data in `data/links.yaml`, linked from the
  footer and Contact page, `/social/` alias); removed a "limited seats"
  line from the calendar page (since superseded: classes now do take sign-ups).
- **PR #46:** fixed leftover "first Thursday" references after another
  session's PR #44 moved classes to Tuesday and added the Dolibarr-backed
  `/classes/` sign-up page. This included the kiosk's fallback schedule,
  which had put the class on the wrong day.

## Vistaprint specs (measured, not from their docs)

Vistaprint's site is blocked from the cloud sessions, so these were measured
from screenshots of their editor's rulers and guides:

- **Tri-fold brochure:** 11.11 x 8.63 in file (bleed 0.055 in left/right,
  0.065 in top/bottom); safe area about 0.125 in inside trim; outside folds
  3.682 in and 7.351 in from the left bleed edge. Inside folds are assumed to
  mirror the outside (how a sheet physically folds) but have **not** been
  checked against their editor.
- **Business card:** 3.61 x 2.11 in (0.055 in bleed per side); safe line
  about 0.06 in inside trim.
- Both HTML files take `?vistaprint`, and `?vistaprint&guides` draws their
  trim, safe and fold lines for checking. Upload the `-vistaprint` PDFs to
  Vistaprint, never the home-print or print-shop ones: Vistaprint stretches
  or crops files that are not exactly its size.

## Still to do or check

- [ ] **SawStop photo.** The woodshop card still uses the general woodshop
  photo. Save a real photo as `assets/photos/sawstop.jpg`, point the
  woodshop `<img>` in `pamphlet.html` at it, rebuild. (Image sites were
  blocked from the session, so it could not be sourced there.)
- [ ] **Vistaprint inside folds.** In their preview, confirm both red fold
  lines fall on panel edges on the inside page too.
- [ ] **Test prints.** Scan every QR code from paper; test the 10-up card
  sheet on plain paper against a card sheet; do a small test cut of the
  yard sign stencil and confirm LightBurn imports it at 24 x 18 in.
- [ ] **Facts to confirm** (see CONTENT.md): the class program and OCA
  credit match the grant agreement (and whether OCA requires its logo), dues,
  and that the people in the cover and robot-arena photos are fine in print.
- [ ] **Laser cutter brand.** The website says OMTech MF2028-80 but the photo
  shows a "Preenex" badge; the pamphlet just says "80 W CO2".
- [ ] **Yard sign logo edges** are slightly wavy because the only logo file is
  a 512 px PNG. An original vector logo would fix that (drop it in and
  replace the tracing step).

## Notes for whoever continues

- **Rebuild after every edit** (`./build.sh`) and look at the preview PNGs;
  the PDFs in `build/` are what people print.
- **Check fit, not just looks.** Panels have fixed heights; a one-word change
  can push the bottom line off a panel. The Vistaprint middle panel is
  0.02 in narrower than the home-print one, so check both versions.
- **Keep facts in sync** across the pamphlet, the card, the website
  (`hugo.toml`, `data/events.yaml`, `data/links.yaml`, `layouts/kiosk.html`)
  and CONTENT.md. The website is the record; other sessions also edit it, so
  fetch `main` before changing it.
- **Website CI** runs `hugo --minify --gc --panicOnWarning` and htmltest. The
  link checker treats redirects as missing pages, so link to real pages.
- **Yard sign build gotchas:** HarfBuzz cannot read the WOFF font directly
  (the script converts it to TTF in memory); the logo PNG has an opaque white
  background, so the orange pixels are selected by color; potracer traces
  `False` pixels, so the mask is passed in inverted.
- **Session network** only reaches package registries (npm, PyPI) and GitHub,
  so new photos, logos or vendor specs have to come from the user.

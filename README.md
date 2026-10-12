# Columbia Gadget Works print materials

A tri-fold pamphlet, a business card, and a yard sign, in the same design language.

## Pamphlet

A printable tri-fold pamphlet for the library and for people taking a tour of
the shop. Ready to print: **[build/pamphlet.pdf](build/pamphlet.pdf)**.

| Outside | Inside |
|---|---|
| ![Outside](build/preview-outside.png) | ![Inside](build/preview-inside.png) |

What is in it, ideas for more, and the pre-print checklist:
[CONTENT.md](CONTENT.md).

### Printing the pamphlet

- US Letter, landscape, **double-sided, flip on short edge**.
- Print at **100% / actual size**, not "fit to page".
- Everything stays 0.3 in from the paper edge, so any office printer works; no bleed is needed.
- Fold as a standard letter fold (tri-fold): the cover is the right-hand panel
  of page 1, and the left-hand panel of page 1 folds in first.
- Print one test copy and scan each QR code before printing a stack.

## Business card

Standard US business card, 3.5 x 2 in, two-sided.
Front: logo, name, and the shop's headline tools. Back: Open Hack Night,
address, website, email, a Discord QR code, and social icons with the
columbiagadgetworks.org/links address.

| Front | Back |
|---|---|
| ![Front](build/preview-card-front.png) | ![Back](build/preview-card-back.png) |

Two print files:

- **[build/business-card.pdf](build/business-card.pdf)**: for a print shop.
  Page 1 is the front, page 2 the back, each 3.75 x 2.25 in including a
  1/8 in bleed on every side (trim to 3.5 x 2 in).
- **[build/business-card-sheet.pdf](build/business-card-sheet.pdf)**: for
  printing in-house on US Letter perforated card sheets with 10 cards per
  sheet (Avery 8371 / 5371 layout). Print double-sided, flip on long edge,
  at 100%. The small tick marks show the cut lines; do a plain-paper test
  first and hold it against a card sheet to check alignment.

## Yard sign

24 x 18 in, for white corrugated plastic (coroplast) sign board, painted
through laser-cut stencils.

![Yard sign](build/yard-sign/preview.png)

Files in `build/yard-sign/`:

- **stencil-rust.svg** and **stencil-dark.svg**: laser files, one per color.
  Red hairlines are the cuts; the blue hairline is the 24 x 18 in sheet
  outline (skip it if the sheet is already cut to size).
- **stencil-one-color.svg**: both layers in one stencil, for a single color.
- **yard-sign.pdf**: full-size color art, if a sign shop prints it instead.

Every stencil is checked for islands when it is built (pieces with no bridge
to the sheet, which would fall out); the build fails if it finds one. The
letters come from Big Shoulders Stencil (SIL Open Font License,
`assets/fonts/`), and the gear is traced from the website logo with four
bridges added across the ring.

Making one:

1. **Stencil material:** 10 mil Mylar (polyester) is reusable and cuts
   cleanly; poster board works for a few signs. Never laser PVC or vinyl.
   A 24 x 18 in sheet fits the shop laser's 28 x 20 in bed. Run a small
   test cut first for power and speed.
2. **Board:** coroplast is polypropylene, so use a spray paint made for
   plastic. Wipe the board with isopropyl alcohol first. For H-stakes, the
   flutes should run up and down (along the 18 in side).
3. **Paint:** tack the stencil down with repositionable spray adhesive so
   paint doesn't creep under the edges. Use light coats, held straight on.
4. **Two colors:** paint the rust stencil, let it dry, then line the dark
   stencil up to the same board edges and paint it. Both stencils are the
   size of the board, so the corners are the registration marks.

## Editing

The pamphlet is `pamphlet.html`, the card is `business-card.html`, and the
yard sign is `scripts/make_yard_sign.py`. Edit there and rebuild:

```bash
pip install -r requirements.txt   # QR codes, yard sign geometry
npm install            # playwright, for rendering to PDF
./build.sh
```

`build.sh` writes the QR codes to `build/qr/` (links are in
`scripts/make_qr.py`), then renders the PDFs and preview images in `build/` with headless
Chromium.

House style: no em dashes, short and plain.

## Design

Borrowed from the CGW website (rust `#BF4D28`, steel, warm paper, Arial,
uppercase eyebrow labels, cards with a rust left rule, the dark photo hero)
and the shop kiosk page (drafting grid background, mono labels, ink-bordered
title blocks).

## Images

All photos are real photos of the shop, copied from the website repository
(`ColumbiaGadgetWorks/website`, `assets/img/`). The gear logo is the
website's `static/img/cgw-gear.png`. Social media icons are the official brand marks from
[Simple Icons](https://simpleicons.org) (CC0), in `assets/icons/`. No AI-generated images or logos are used;
keep it that way when swapping photos.

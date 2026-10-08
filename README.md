# Columbia Gadget Works pamphlet

A printable tri-fold pamphlet for the library and for people taking a tour of
the shop. Ready to print: **[build/pamphlet.pdf](build/pamphlet.pdf)**.

| Outside | Inside |
|---|---|
| ![Outside](build/preview-outside.png) | ![Inside](build/preview-inside.png) |

What is in it, ideas for more, and the pre-print checklist:
[CONTENT.md](CONTENT.md).

## Printing

- US Letter, landscape, **double-sided, flip on short edge**.
- Print at **100% / actual size**, not "fit to page".
- Everything stays 0.3 in from the paper edge, so any office printer works; no bleed is needed.
- Fold as a standard letter fold (tri-fold): the cover is the right-hand panel
  of page 1, and the left-hand panel of page 1 folds in first.
- Print one test copy and scan each QR code before printing a stack.

## Editing

The pamphlet is one HTML file, `pamphlet.html`. Edit the text there and rebuild:

```bash
pip install segno      # QR codes
npm install            # playwright, for rendering to PDF
./build.sh
```

`build.sh` writes the QR codes to `build/qr/` (links are in
`scripts/make_qr.py`), then renders `build/pamphlet.pdf` and the two preview
images with headless Chromium.

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

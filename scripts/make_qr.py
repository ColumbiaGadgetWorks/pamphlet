"""Draw the pamphlet's QR codes as SVG files in build/qr/.

The links are the same ones the website uses (hugo.toml in
ColumbiaGadgetWorks/website). Change them here if they ever change there.
"""
import pathlib
import segno

LINKS = {
    "discord": "https://discord.gg/yjpeBrAjuR",
    "website": "https://columbiagadgetworks.org/",
    "wiki": "https://wiki.comogadget.casa/",
    "calendar": "https://columbiagadgetworks.org/calendar/",
    "donate": "https://columbiagadgetworks.org/donate/",
}

out = pathlib.Path(__file__).resolve().parent.parent / "build" / "qr"
out.mkdir(parents=True, exist_ok=True)
for name, url in LINKS.items():
    # Error correction "M" plus a 4-module quiet zone scans reliably off paper.
    segno.make(url, error="m").save(out / f"{name}.svg", scale=10, border=4, dark="#1F1F23", xmldecl=False)
    print(f"build/qr/{name}.svg  {url}")

// Render the print files and PNG previews into build/:
//   pamphlet.html       -> pamphlet.pdf (two letter-size landscape pages)
//   business-card.html  -> business-card.pdf (front and back, with bleed)
//                          business-card-sheet.pdf (letter, 10 per side)
//   build/yard-sign/*.svg -> yard-sign/yard-sign.pdf (24 x 18 in) and previews
const { chromium } = require("playwright");
const path = require("node:path");

const root = path.resolve(__dirname, "..");
const build = (name) => path.join(root, "build", name);
const fileUrl = (name, query = "") => "file://" + path.join(root, name) + query;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1056, height: 816 }, deviceScaleFactor: 2 });
  const pdf = (name) => page.pdf({ path: build(name), printBackground: true, preferCSSPageSize: true });

  await page.goto(fileUrl("pamphlet.html"), { waitUntil: "networkidle" });
  await pdf("pamphlet.pdf");
  const sides = await page.$$(".sheet");
  const names = ["outside", "inside"];
  for (let i = 0; i < sides.length; i++) {
    await sides[i].screenshot({ path: build(`preview-${names[i]}.png`) });
  }

  await page.goto(fileUrl("business-card.html"), { waitUntil: "networkidle" });
  await pdf("business-card.pdf");
  const cards = await page.$$(".card");
  for (const [i, side] of ["front", "back"].entries()) {
    await cards[i].screenshot({ path: build(`preview-card-${side}.png`) });
  }

  await page.goto(fileUrl("business-card.html", "?sheet"), { waitUntil: "networkidle" });
  await pdf("business-card-sheet.pdf");

  // Yard sign: the art SVG is drawn at real size (24 x 18 in = 2304 x 1728 px).
  const sign = await browser.newPage({ viewport: { width: 2304, height: 1728 }, deviceScaleFactor: 0.5 });
  await sign.goto(fileUrl("build/yard-sign/yard-sign.svg"));
  await sign.screenshot({ path: build("yard-sign/preview.png") });
  await sign.pdf({ path: build("yard-sign/yard-sign.pdf"), width: "24in", height: "18in", printBackground: true, pageRanges: "1" });

  await browser.close();
  console.log("build/: pamphlet.pdf, business-card.pdf, business-card-sheet.pdf, yard-sign/, preview PNGs");
})();

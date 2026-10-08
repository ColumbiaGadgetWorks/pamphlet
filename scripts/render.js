// Render the print files and PNG previews into build/:
//   pamphlet.html       -> pamphlet.pdf (two letter-size landscape pages)
//   business-card.html  -> business-card.pdf (front and back, with bleed)
//                          business-card-sheet.pdf (letter, 10 per side)
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

  await browser.close();
  console.log("build/: pamphlet.pdf, business-card.pdf, business-card-sheet.pdf, preview PNGs");
})();

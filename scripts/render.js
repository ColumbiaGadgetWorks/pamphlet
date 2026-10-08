// Render pamphlet.html to build/pamphlet.pdf (two letter-size landscape
// pages) and a PNG preview of each side.
const { chromium } = require("playwright");
const path = require("node:path");

const root = path.resolve(__dirname, "..");
const url = "file://" + path.join(root, "pamphlet.html");

(async () => {
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1056, height: 816 }, deviceScaleFactor: 2 });
await page.goto(url, { waitUntil: "networkidle" });

await page.pdf({ path: path.join(root, "build", "pamphlet.pdf"), width: "11in", height: "8.5in", printBackground: true, preferCSSPageSize: true });

const sides = await page.$$(".sheet");
const names = ["outside", "inside"];
for (let i = 0; i < sides.length; i++) {
  await sides[i].screenshot({ path: path.join(root, "build", `preview-${names[i]}.png`) });
}
await browser.close();
console.log("build/pamphlet.pdf, build/preview-outside.png, build/preview-inside.png");
})();

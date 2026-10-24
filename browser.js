const fs = require("node:fs");
const { chromium } = require("playwright");

const DEFAULT_EXECUTABLE = "/data/data/com.termux/files/usr/lib/chromium/chrome";

function resolveExecutablePath() {
  const configured = process.env.CHROMIUM_PATH;
  if (configured) return configured;
  if (fs.existsSync(DEFAULT_EXECUTABLE)) return DEFAULT_EXECUTABLE;
  return undefined;
}

async function scrapePage(url) {
  if (typeof url !== "string" || !/^https?:\/\//i.test(url)) {
    throw new TypeError("url must be an absolute http(s) URL");
  }

  const browser = await chromium.launch({
    headless: true,
    executablePath: resolveExecutablePath(),
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  try {
    const page = await browser.newPage();
    await page.goto(url, {
      waitUntil: "domcontentloaded",
      timeout: 30_000,
    });

    return {
      title: await page.title(),
      url: page.url(),
      text: await page.locator("body").innerText(),
    };
  } finally {
    await browser.close();
  }
}

module.exports = { scrapePage };

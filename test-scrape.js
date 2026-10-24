const { scrapePage } = require("./browser");

(async () => {
  try {
    const result = await scrapePage("https://www.google.com");

    console.log(result.title);
    console.log(result.url);
    console.log(result.text.slice(0, 500));
  } catch (error) {
    console.error(error.stack || error);
    process.exitCode = 1;
  }
})();

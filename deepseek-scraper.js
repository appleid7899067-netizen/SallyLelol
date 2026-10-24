const fetch = require('node-fetch');
const cheerio = require('cheerio');

// Webhook - clone deepseek.com
const API_URL = 'https://chat.deepseek.com';

(async () => {
  // 1. Fetch page 
  const response = await fetch(API_URL, {
    headers: { 'Accept': 'application/json' }
  });
  if (!response.ok) {
    console.error(`Failed to fetch (${response.status})`);
    process.exit(1);
  }
  const html = await response.text();

  // 2. Parse with cheerio
  const $ = cheerio.load(html);

  console.log('=== DeepSeek Scraper Result ===');
  console.log('Title:', $(document).css('title'));
  console.log('Is prompt input present?', !!$(('textarea[name="prompt"]["data-input"]").length));
  console.log('Page length:', html.length);
})();

# Puter OpenAI/GPT Pricing (22 October 2026)

> Source: https://developer.puter.com/ai/models/ ; https://developer.puter.com/pricing ; https://puter.com/pricing ; https://docs.puter.com/rate-limits-and-quotas/index.md ; https://docs.puter.com/AI/listModels/index.md

Puter AI follows a user-pays model: an app using Puter.js does not need to pay a developer API-key bill, but AI usage is charged against the signed-in user's Puter allowance or credits. A monthly free allowance exists but its exact monetary/token amount is displayed in the user dashboard rather than fixed on the public pricing page. Exhausted allowance/credits may result in `402 insufficient_funds`.

## Confirmed OpenAI prices

Prices shown in Puter's live model directory, USD per 1M tokens:

| Puter model ID | Input | Output |
|---|---:|---:|
| `openai/gpt-6-luna` | $0.10 | $0.50 |
| `openai/gpt-6-luna-pro` | $0.10 | $0.50 |
| `openai/gpt-6-sol` | $2.00 | $10.00 |
| `openai/gpt-6-sol-pro` | $2.00 | $10.00 |
| `openai/gpt-6.1-sol` | $2.00 | $10.00 |
| `openai/gpt-6.1-sol-pro` | $2.00 | $10.00 |

Puter prices are live-catalogue values and can change. Query `puter.ai.listModels()` to retrieve currently exposed models and their costs programmatically.

## Access and limits

- Puter.js AI methods (for example `puter.ai.chat()`) are available to account types subject to allowance, credits, and rate limits.
- Puter's OpenAI-compatible REST endpoint requires a paid subscription; free accounts receive `402 subscription_required`.
- Public plans: Free $0/month, Basic $10/month, Plus $25/month, Pro $100/month. Public pages describe AI capacity qualitatively and do not publish a fixed per-model included token quota.
- AI rate limits per user and per app: Free 30 requests/10 seconds and 3 concurrent requests; Paid 200 requests/10 seconds and 20 concurrent requests; guest 20 requests/10 seconds and 2 concurrent requests.

## Practical interpretation

Puter can let an application call supported GPT/OpenAI models without managing an OpenAI key, initially using each user's monthly Puter allowance. It is not unlimited free GPT; after allowance is consumed, the user must top up credits or upgrade.

## Related

- [Free Model Routing](../analysis/free-model-routing-2026-10.md) — prior NovaAgent observations about Puter availability.
- [OpenAI API Pricing (22 October 2026)](openai-api-pricing-2026-10-22.md) — direct OpenAI pricing snapshot for comparison.

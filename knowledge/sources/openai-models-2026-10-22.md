# OpenAI model families and selectable model names — 2026-10-22

> Research date: 2026-10-22 (UTC+07). Sources are first-party OpenAI pages only: `platform.openai.com/docs`, `openai.com`, and `help.openai.com`.

## Executive summary

OpenAI's current API model landing page recommends three general-purpose models: **GPT-6 Astra** (`gpt-6-astra`) for the hardest reasoning and coding, **GPT-6.1 Sol** (`gpt-6.1-sol`) for a quality/cost balance, and **GPT-6 Luna** (`gpt-6-luna`) for efficient, high-volume work. The same page says the latest models support text and image input, text output, multilingual use, and the Responses API/SDKs.

For practical application selection, the main families are:

- **GPT-6 flagship family:** Astra, 6.1 Sol, Luna; the current default starting points.
- **GPT-5.x general-purpose/reasoning and coding family:** still listed in the full catalog, but several entries are explicitly described as previous/succeeded models rather than the newest defaults.
- **GPT-4.1 family:** non-reasoning models useful where predictable, fast general text/code behavior is preferred.
- **Realtime/audio, image, embeddings, moderation, and specialized models:** purpose-built model families rather than substitutes for the flagship text models.

The API catalog is not a pure “currently recommended” list: it includes historical, deprecated, and compatibility models. Always check the individual model page and deprecations page before hard-coding a model ID.

## 1. Current general-purpose models

| Model | Model ID | Best fit | Practical use |
|---|---|---|---|
| **GPT-6 Astra** | `gpt-6-astra` | Highest capability; complex reasoning and coding | Difficult analysis, ambitious deliverables, complex software engineering, agentic workflows, computer-use tasks where quality matters most |
| **GPT-6.1 Sol** | `gpt-6.1-sol` | Near-Astra performance at lower cost | Professional work, technical projects, coordinated deliverables, research/analysis where cost and quality both matter |
| **GPT-6 Luna** | `gpt-6-luna` | Most efficient flagship option | High-volume automation, triage, scoped tasks, extraction, routine coding and editing; a sensible low-cost default |

The model page lists these models with configurable reasoning effort. It lists approximately 1.05M-token context windows and 128K maximum output for each featured model, but exact limits, pricing, tools, and availability can change by endpoint/product. The current API docs explicitly recommend Astra when unsure, Sol to balance intelligence and cost, and Luna for cost-sensitive high-volume workloads.

**About “Luna”:** The current featured model is `gpt-6-luna`. The full catalog also lists `gpt-5.6-luna`; that is a different older GPT-5.6-class model. An app label such as “Luna” may be an app/provider alias, so verify the actual model ID in the app or API request.

## 2. GPT-5.x family (catalog and compatibility models)

The full official catalog lists these names. They are useful when an integration, benchmark, or product specifically requires them, but the catalog labels several as previous/succeeded models, so they should not automatically be treated as the newest recommendation:

- **GPT-5:** `gpt-5` — previous intelligent reasoning model for coding and agentic tasks, with configurable reasoning effort.
- **GPT-5 Mini:** `gpt-5-mini` — strong intelligence for cost-sensitive, low-latency, high-volume workloads.
- **GPT-5 nano:** `gpt-5-nano` — fastest and most cost-efficient GPT-5 variant.
- **GPT-5 Pro:** `gpt-5-pro` — more compute for smarter, more precise answers.
- **GPT-5.1:** `gpt-5.1` — coding and agentic tasks with configurable reasoning effort.
- **GPT-5.2:** `gpt-5.2` — previous flagship for professional work; configurable reasoning effort.
- **GPT-5.2 Pro:** `gpt-5.2-pro` — previous pro model for professional work.
- **GPT-5.4:** `gpt-5.4` — more affordable coding and professional work.
- **GPT-5.4 Mini:** `gpt-5.4-mini` — coding, computer use, and subagents.
- **GPT-5.4 nano:** `gpt-5.4-nano` — cheapest GPT-5.4-class model for simple high-volume tasks.
- **GPT-5.4 Pro:** `gpt-5.4-pro` — more precise GPT-5.4 variant.
- **GPT-5.5:** `gpt-5.5` — coding and professional work.
- **GPT-5.5 Pro:** `gpt-5.5-pro` — more precise GPT-5.5 variant.
- **GPT-5.6 Sol:** `gpt-5.6-sol` — GPT-5.6 flagship for complex professional work.
- **GPT-5.6 Terra:** `gpt-5.6-terra` — GPT-5.6 model balancing intelligence and cost.
- **GPT-5.6 Luna:** `gpt-5.6-luna` — GPT-5.6 model optimized for cost-sensitive workloads.

ChatGPT-facing aliases are also catalogued, including `gpt-5-chat-latest`, `gpt-5.1-chat-latest`, `gpt-5.2-chat-latest`, and `gpt-5.3-chat-latest`. These are product aliases, not necessarily the best stable IDs for a new API integration.

Coding-specialized variants include `gpt-5-codex`, `gpt-5.1-codex`, `gpt-5.1-codex-mini`, `gpt-5.1-codex-max`, `gpt-5.2-codex`, and `gpt-5.3-codex`. Use them when building Codex-oriented, long-horizon, agentic coding workflows; otherwise start with the current flagship catalog recommendation.

## 3. GPT-4.1 family

- **GPT-4.1** — `gpt-4.1`: official catalog description is “smartest non-reasoning model.” Good for ordinary text/code generation, instruction following, structured transformations, and predictable low-latency application flows where explicit extended reasoning is not needed.
- **GPT-4.1 Mini** — `gpt-4.1-mini`: smaller, faster GPT-4.1 variant; useful for higher-throughput assistants, classification/extraction, and cost-sensitive applications.
- **GPT-4.1 nano** — `gpt-4.1-nano`: fastest and most cost-efficient GPT-4.1 variant; useful for simple routing, tagging, extraction, and very high-volume calls.

The catalog also still lists GPT-4o (`gpt-4o`), GPT-4o Mini (`gpt-4o-mini`), GPT-4 (`gpt-4`), GPT-4 Turbo (`gpt-4-turbo`), and related audio/search/realtime variants. These are compatibility choices rather than the first models to choose for a new general-purpose integration unless a product requirement says otherwise.

## 4. Reasoning and deep-research models

The catalog lists the o-series, but labels the main entries as succeeded by GPT-5 or previous:

- `o3` — complex-task reasoning; catalog says succeeded by GPT-5.
- `o4-mini` — fast, cost-efficient reasoning; catalog says succeeded by GPT-5 Mini.
- `o3-pro` and `o1-pro` — more-compute variants for higher-quality responses.
- `o3-deep-research` — powerful deep-research model.
- `o4-mini-deep-research` — faster, more affordable deep-research model.
- `o1`, `o1-mini`, `o1-preview`, and `o3-mini` — older/previous reasoning choices, generally compatibility options.

For a new general reasoning workflow, the current docs point users toward GPT-6 Astra/Sol/Luna and configurable reasoning effort. Use the deep-research-specific IDs only when the API/product workflow explicitly supports that specialized task.

## 5. Realtime, speech, and audio

These models are for voice or audio pipelines, not ordinary text-only completion:

- **Realtime conversation:** `gpt-realtime-2.1`, `gpt-realtime-2.1-mini`, `gpt-realtime-2`, `gpt-realtime-1.5`, and `gpt-realtime-mini` are catalogued for realtime text/audio input and output; the Realtime guide's current example uses `gpt-realtime-2.1` for low-latency, interruptible voice agents with tools.
- **Realtime translation:** `gpt-realtime-translate` for streaming speech-to-speech translation.
- **GPT-Live:** `gpt-live-1` for natural, expressive voice conversations with smooth interruption handling.
- **Transcription:** `gpt-transcribe` is the recommended model for completed audio files. `gpt-live-transcribe` is the current low-latency live transcription path; `gpt-realtime-whisper` is also catalogued for streaming transcription.
- **Text to speech:** `gpt-4o-mini-tts` is still documented for the Speech API, but the official guide says `tts-1`, `tts-1-hd`, and `gpt-4o-mini-tts` are deprecated and scheduled to shut down on 2027-01-06; new realtime voice work should migrate to `gpt-realtime-2.1-mini` via Realtime rather than treating it as a drop-in `/v1/audio/speech` replacement.

The transcription guide states that `whisper-1`, `gpt-4o-transcribe`, `gpt-4o-mini-transcribe`, and `gpt-4o-transcribe-diarize` are deprecated and scheduled to shut down on 2027-02-26. For new file transcription use `gpt-transcribe`; for live microphone/call streams use the Realtime transcription workflow.

## 6. Image-generation models

- **GPT-Image-2.5 Sunburst** — `gpt-image-2.5-sunburst`: most capable image generation/editing model in the current catalog.
- **GPT-Image-2.5 Flare** — `gpt-image-2.5-flare`: faster, high-quality everyday image generation.
- **GPT-Image-2** — `gpt-image-2`: state-of-the-art image generation model in the catalog.
- `gpt-image-1.5`, `gpt-image-1`, and `gpt-image-1-mini` are listed as previous or cost-efficient image models; use for compatibility or cost-specific requirements after checking their individual status.

Use these for creating/editing images, rather than selecting Astra/Sol/Luna and expecting a text model to produce image pixels.

## 7. Embeddings and moderation

- **Embeddings:** `text-embedding-3-large` (highest capability) and `text-embedding-3-small` (smaller/cheaper). Use for semantic search, retrieval, clustering, recommendations, classification features, and RAG indexes. `text-embedding-ada-002` is an older model.
- **Moderation:** `omni-moderation-latest` is the current multimodal moderation model in the catalog. Older `text-moderation` and `text-moderation-stable` entries are previous-generation text-only models.

These models do not replace a general chat/reasoning model: embeddings return vectors, and moderation classifies potentially harmful content.

## 8. Specialized and open-weight models

- **Cybersecurity:** `gpt-5.6-cyber` and Daybreak aliases (`gpt-daybreak-blue-latest`, `gpt-daybreak-red-latest`) are specialized for authorized defensive security, vulnerability research, and testing. Treat access as product/organization-dependent.
- **Life sciences:** `gpt-rosalind-research` / GPT-Rosalind is listed for approved organizations; access is specialized rather than general API availability.
- **Open-weight:** `gpt-oss-120b` and `gpt-oss-20b` are catalogued as open-weight models for self-hosted/low-latency use cases, not the same hosted API choice as GPT-6.
- **Computer use:** `computer-use-preview` is a specialized compatibility model for the computer-use tool; prefer the current flagship models when the current product workflow supports computer use directly.

## What to choose in practice

1. **General assistant, coding, analysis, or agent:** start with `gpt-6-astra` for maximum quality, `gpt-6.1-sol` for the usual quality/cost balance, or `gpt-6-luna` for volume and low cost.
2. **Simple high-volume classification/extraction:** consider GPT-6 Luna, GPT-5.4 nano, GPT-5 nano, or GPT-4.1 nano only after evaluating quality and current availability.
3. **Non-reasoning, predictable text/code transformation:** GPT-4.1 family remains a practical choice when its behavior/latency/cost fit the application.
4. **Voice agent:** use the Realtime family and Realtime API; do not build a new voice agent around deprecated audio models.
5. **Recorded speech:** use `gpt-transcribe`; live speech uses `gpt-live-transcribe`/Realtime workflow.
6. **Images:** use the current GPT-Image family.
7. **RAG/search index:** use `text-embedding-3-small` for economical scale or `text-embedding-3-large` for higher retrieval quality; pair with a general model for answer generation.
8. **Safety filtering:** use `omni-moderation-latest` before/after generation as appropriate.

## Official-source uncertainty and conflicts

- The API landing page presents GPT-6 Astra/Sol/Luna as the current featured choices, while the full catalog simultaneously lists many GPT-5.x, GPT-4.x, o-series, and historical entries. This is a catalog/compatibility distinction, not evidence that every listed model is equally recommended or equally available.
- The full catalog uses “GPT-6.1 Sol” in the featured section but also lists `gpt-6-sol`; the model-selection page likewise names GPT-6.1 Sol. The safe current selection is the explicitly featured ID `gpt-6.1-sol` unless the API model catalog for the account says otherwise.
- The catalog's specialized-model names and availability can be organization-, endpoint-, or product-dependent. Confirm access using the account's live model catalog.
- The docs use both `platform.openai.com/docs` and newer `developers.openai.com/api/docs` links in extracted pages. They are OpenAI first-party documentation, but this note follows the requested official-source policy and cites the platform/openai/help domains below.

## Sources

1. [OpenAI API — Models](https://platform.openai.com/docs/models) — featured models, model IDs, capabilities, and full catalog.
2. [OpenAI API — Model selection](https://platform.openai.com/docs/guides/model-selection) — practical model-selection guidance and reasoning-effort guidance.
3. [OpenAI API — Realtime API getting started](https://platform.openai.com/docs/guides/realtime) — current speech-to-speech voice-agent workflow and `gpt-realtime-2.1` example.
4. [OpenAI API — File transcription](https://platform.openai.com/docs/guides/speech-to-text) — recommended `gpt-transcribe` and transcription deprecations/timelines.
5. [OpenAI API — Text to speech](https://platform.openai.com/docs/guides/text-to-speech) — TTS models, current deprecation timeline, and migration guidance.
6. [OpenAI API — Vector embeddings](https://platform.openai.com/docs/guides/embeddings) — embedding models and search/retrieval use cases.
7. [OpenAI API — Deprecations](https://platform.openai.com/docs/deprecations) — official lifecycle/deprecation status to check before production selection.
8. [OpenAI Help Center — Model release notes](https://help.openai.com/en/articles/9624314-model-release-notes) — official release/deprecation context; page access was restricted during this retrieval, so claims above prioritize the accessible API documentation.

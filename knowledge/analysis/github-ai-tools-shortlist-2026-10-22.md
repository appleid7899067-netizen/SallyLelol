# GitHub AI Tools Shortlist — 22 ตุลาคม 2026

## ขอบเขตและวิธีคัดเลือก

คัดเลือกจาก repository และเอกสารทางการของโครงการเป็นหลัก โดยดูการบำรุงรักษา ความพร้อมใช้งานจริง การรองรับ local/API ความปลอดภัย ใบอนุญาต และความเหมาะกับ NovaAgent/คอมพิวเตอร์บ้าน จำนวนดาวใช้เป็นสัญญาณขนาด ecosystem เท่านั้น ไม่ใช่หลักฐานคุณภาพเพียงอย่างเดียว

## คำตอบสั้นที่สุด

### ชุดเริ่มต้นสำหรับคอมบ้าน

```text
Ollama → Open WebUI
```

- **Ollama**: runtime/API สำหรับรันโมเดล local
- **Open WebUI**: หน้าตาแบบ ChatGPT, RAG, file upload, tools, MCP, web search และต่อ OpenAI-compatible API
- ถ้าเน้นเอกสาร/ฐานความรู้เป็นหลัก ให้พิจารณา **AnythingLLM**
- ถ้าต้องการ desktop GUI ที่ติดตั้งง่าย ให้ดู **Jan** หรือ **LM Studio**
- ถ้าต้องการหลายผู้ใช้และหลาย provider ให้ดู **LibreChat**

## อันดับแพลตฟอร์ม Local AI

1. **Ollama + Open WebUI** — สมดุลดีที่สุดสำหรับผู้ใช้ส่วนใหญ่; local, API, UI และ ecosystem ครบ
2. **AnythingLLM** — เด่นสุดด้าน PDF/DOCX, workspace, citations, RAG และ agent ส่วนตัว; MIT
3. **LibreChat** — เหมาะกับ multi-provider/multi-user, OAuth, agents และ cloud API; MIT แต่ตั้งค่าซับซ้อนกว่า
4. **Jan** — desktop local AI ที่ offline ได้และ license ชัดเจน Apache-2.0
5. **LM Studio** — desktop experience ง่ายที่สุดและเปิด local OpenAI-compatible server แต่ตัวแอปหลักไม่ได้ open source ทั้งหมด
6. **llama.cpp** — runtime ระดับลึกสำหรับ power users; MIT, รองรับ backend/hardware กว้าง
7. **LocalAI** — API server สำหรับ text, vision, audio, image และ embedding; เหมาะกับงานหลาย modality แต่ซับซ้อนกว่า Ollama

แหล่งทางการ:

- https://github.com/ollama/ollama
- https://github.com/open-webui/open-webui
- https://github.com/Mintplex-Labs/anything-llm
- https://github.com/LibreChat-AI/LibreChat
- https://github.com/janhq/jan
- https://github.com/lmstudio-ai
- https://github.com/ggml-org/llama.cpp
- https://github.com/mudler/LocalAI

## อันดับ Coding Agents

1. **Cline** — ตัวเลือกครบสุดสำหรับ IDE/terminal; รองรับ Ollama, LM Studio, OpenAI-compatible API, MCP และมี approval/diff/checkpoint
2. **OpenCode** — terminal-first, open source, MIT, มี plan/read-only mode และ permission model; เหมาะกับระบบที่ต้องการควบคุม
3. **Goose** — agent ทั่วไปสำหรับ coding, research, data และ automation; รองรับ Ollama/provider มากกว่า 15 ราย; Apache-2.0
4. **Aider** — mature Git-centric pair programmer; เหมาะที่สุดกับ repository ที่ต้องการ diff, commit, lint และ test ที่ตรวจสอบได้; Apache-2.0
5. **OpenHands / Agent Canvas** — control plane สำหรับ agent server, Docker sandbox, scheduled automation และหลาย backend; powerful แต่ต้องตั้ง sandbox จริง
6. **Codex CLI** — ตัวเลือกทางการของ OpenAI; ดีเมื่อผูกกับ OpenAI/ChatGPT แต่ไม่ใช่ abstraction layer สำหรับ local หลาย provider
7. **mini-SWE-agent** — core เล็ก ตรวจสอบง่าย เหมาะกับ benchmark และสร้าง runner ของ NovaAgent; MIT

### ไม่ควรเริ่มโปรเจกต์ใหม่ด้วย

- **Continue** — repository ระบุว่าไม่ active และ read-only
- **Roo Code** — repository archived และ extension ปิดแล้ว
- **SWE-agent รุ่นเก่า** — maintainers แนะนำ mini-SWE-agent สำหรับงานใหม่

แหล่งทางการ:

- https://github.com/cline/cline
- https://github.com/anomalyco/opencode
- https://github.com/aaif-goose/goose
- https://github.com/Aider-AI/aider
- https://github.com/OpenHands/OpenHands
- https://github.com/openai/codex
- https://github.com/SWE-agent/mini-swe-agent
- https://github.com/continuedev/continue
- https://github.com/RooCodeInc/Roo-Code

## อันดับ Infrastructure สำหรับระบบ AI จริง

1. **LiteLLM** — gateway รวม OpenAI, Anthropic, Gemini, Ollama, vLLM และ provider อื่น; routing, fallback, keys และ spend tracking
2. **vLLM** — production model serving บน GPU, batching และ OpenAI-compatible API; Apache-2.0
3. **Haystack** — RAG/orchestration แบบ explicit และ testable; Apache-2.0
4. **LlamaIndex** — document ingestion, connectors, indexing และ RAG toolkit; MIT; แยก framework ฟรีออกจากบริการ LlamaParse
5. **LangGraph** — stateful agent runtime ที่มี checkpoint, retry, persistence และ human-in-the-loop; MIT
6. **Crawl4AI** — self-hosted web crawling/Markdown/JSON extraction สำหรับ RAG; Apache-2.0
7. **SearXNG** — privacy-preserving metasearch; AGPL-3.0; ควรใช้คู่กับ crawler
8. **Firecrawl** — search/scrape/crawl/map/parse API ครบกว่า แต่ self-host และ cloud มีความสามารถ/ต้นทุนต่างกัน; หลักเป็น AGPL-3.0
9. **Langfuse** — self-hosted tracing, prompts, datasets และ evaluations; MIT ยกเว้นส่วน enterprise
10. **Phoenix** — OpenTelemetry/OpenInference tracing และ evaluation; แข็งแรง แต่ใช้ ELv2 ต้องอ่านเงื่อนไข

แหล่งทางการ:

- https://github.com/BerriAI/litellm
- https://github.com/vllm-project/vllm
- https://github.com/deepset-ai/haystack
- https://github.com/run-llama/llama_index
- https://github.com/langchain-ai/langgraph
- https://github.com/unclecode/crawl4ai
- https://github.com/searxng/searxng
- https://github.com/firecrawl/firecrawl
- https://github.com/langfuse/langfuse
- https://github.com/Arize-ai/phoenix

## สแตกที่แนะนำสำหรับ NovaAgent

### ระยะที่ 1: ใช้งานจริงแบบไม่บวม

```text
Ollama
└── Open WebUI

Aider — งานแก้ repository แบบมี Git review
Cline หรือ OpenCode — งาน interactive/agent
```

### ระยะที่ 2: ต่อหลาย provider และตรวจสอบต้นทุน

```text
Providers (Ollama/OpenAI/Anthropic/Gemini/...)
└── LiteLLM
    ├── Open WebUI
    ├── Cline/OpenCode
    └── NovaAgent
```

### ระยะที่ 3: RAG และ web intelligence

```text
SearXNG → Crawl4AI → Haystack/LlamaIndex
                         └── LangGraph สำหรับ stateful workflows
```

### ระยะที่ 4: production/automation

```text
vLLM (GPU serving) + LiteLLM (gateway)
OpenHands (sandboxed orchestration)
Langfuse หรือ Phoenix (tracing/evaluation)
```

## คำตัดสิน

ถ้าต้องเลือก “ดีที่สุด” เพียงชุดเดียวสำหรับคอมบ้าน: **Ollama + Open WebUI**

ถ้าต้องเลือกเครื่องมือ coding หลักของ NovaAgent: **Aider เป็น baseline ที่ควบคุมง่าย** และ **Cline เป็น interactive agent ที่ครบที่สุด**; หากให้ความสำคัญกับ MIT/terminal/read-only planning มาก ให้เลือก **OpenCode**

ถ้าต้องสร้างระบบระยะยาว: เพิ่ม **LiteLLM** เป็น provider gateway, **LangGraph** เป็น stateful workflow runtime, **Crawl4AI + SearXNG** สำหรับเว็บ และ **Langfuse** สำหรับ observability

## ความปลอดภัยขั้นต่ำ

- ใช้ approval mode และ read-only plan ก่อน write mode
- รัน agent ใน disposable worktree หรือ container
- mount เฉพาะ repository เป้าหมาย ไม่ mount home directory
- ห้ามให้ `.env`, SSH keys, browser profile หรือ production credentials
- จำกัด MCP และ network ด้วย allowlist
- อย่า expose Ollama/OpenAI-compatible API ตรงสู่ Internet โดยไม่มี authentication
- pin release/version ใน production แทนการใช้ `main` หรือ rolling image
- ตรวจ license โดยเฉพาะ Open WebUI, AGPL และ ELv2 ก่อนแจกจ่ายเชิงพาณิชย์

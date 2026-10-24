# OpenCode Competitive Analysis (25 ตุลาคม 2026)

**เป้าหมาย:** แกะ OpenCode (opencode.ai) เพื่อกำหนดตำแหน่ งและแนวทางการออกแบบ NovaAgent web ให ้"ข่ม" ได ้

---

## 🧩 สถานะความเป็นจริง (Fact Check)

| ประเด็น | ความจริง |
|---|---|
| **opencode.ai** | โปรเจกต ์ V2 โดย Anomaly (anomalyco/opencode) — 221K stars, 29.5K forks, 20,856 commits |
| **V1 (opencode-ai/opencode)** | Terminal TUI (Go + Bubble Tea) — **ถูก archive 18 ก.ย. 2025** ย ้ายไปทำ "Crush" กับท ีม Charm |
| **V2 คืออะไร** | Coding agent แบบครบวงจร: CLI + Desktop App (BETA) + Web Console (SaaS) |
| **Desktop stack** | Electron 44 + SolidJS + electron-vite + Turborepo monorepo + Effect + Drizzle + Sentry |
| **API** | 139 endpoints (V2_HTTP_API_AUDIT.md, regenerate 2026-09-13) — session, PTY, filesystem, VCS, MCP, permissions |
| **Console** | SaaS แยกต ่างหาก (opencode.ai/console) — login via Google/GitHub/email, workspaces, members, SSO, SCIM, budgets, billing |
| **Zen** | Managed model service — "curated optimized models", pay-per-request, มี testimonials, privacy claims |
| **Data page** | Public model-usage leaderboard — 26T tokens/วัน (peak), retention, session cost, geo breakdown (จีน 14%, US 12%, อินเดีย 6%) |
| **Localization** | README 24 ภาษา (มีไทย) — community-driven translation |

---

## 🏗️ สิ่งที่เขามี (Strengths — ต้องยอมรับ)

1. **Scale & momentum จริ ง** — 221K stars, 412K peak daily users, 26T tokens/วัน
2. **Product ครบชั้ น** — CLI, desktop, web console, HTTP API, managed models (Zen)
3. **Engineering discipline สู ง** — API audit checklist 139 endpoints, V2_HTTP_API_AUDIT.md, type-safe contracts
4. **Data transparency** — /data เปิ ด model usage จริง ให้คนดูได ้ (marketing + trust ไปในตัว)
5. **Ecosystem lock-in** — MCP, plugins, skills, commands, agents (build/plan), worktrees
6. **Community machine** — 24 ภาษา, Discord, changelog, contributer 950+ คน

---

## 💔 จุดอ่ อน (Weaknesses — ช่ องว่ างของเรา)

### 1. Homepage เป็น generic SaaS template
- Headline "The open source AI coding agent" ซ้ ำ 2 ครั้ง (hero + section ที่ 2)
- Layout ดู "ไดโนเสาร์เทมเพลต" — ไม่มีบุคลิก, ไม่มีตัวตน
- Social proof ยัดเยียด: 220K stars / 950 contributors / 16M devs / 20K commits — ดูกู้ ego เกินจำเป็น
- Newsletter waitlist "Be the first to know when we release new products" — แสดงว่ ายังไม่มี product จริงในบางส่ วน

### 2. CTA แตกทิศ 4 ทาง
Download · Read docs · Learn about Zen · Subscribe — ไม่มุ่ งจุดเดียว

### 3. Privacy claim ขัดแย้งในตัวเอง
- Homepage: "Built for privacy first"
- Zen FAQ: "data stored when using free models" — มีข้อยกเว้ น (ดู /v2/docs/console/models/#privacy)
- **นี่คือ contradiction ที่ NovaAgent ข่มได ้โดยเปิ ดอกเปิ ดใจ** — เราบอกตรงๆ ว่ าอะไรเก็ บ อะไรไม่เก็ บ

### 4. Messaging ซ้ำซ้อน
- "What is OpenCode?" มีทั้งใน hero section แล ะ FAQ
- Zen ซ้ำ concept "optimized models" หลายรอบ + testimonials ที่ดูซื้ อ/จัดมา (ex-CEO, ex-Founder...)

### 5. Desktop = Electron บวม
- Electron 44.9.1 + SolidJS — หนัก, กิน RAM, startup ช้า
- **NovaAgent Browser-first บน Termux/Android เบากว่ า และเป็ น "เดสก ์ท็อปที่สอง" แบบเรียลไทม์ได ้**

### 6. Terminal-first mindset ยังเหนียว
- V2 ยังเขียน "Built for the terminal" ใน README
- Console เป็ น SaaS แยก — ไม่ใช่ desktop experience ที่ต่ อเนื่อง

### 7. ไม่มี "ตัวตน" ของ AI
- OpenCode คือ **เครื่ องมือเย็ นชา** — ไม่ม ี persona, ไม่ evolve, ไม่รู ้จักบอส
- ขาดความเป็ น "partner" โดยสิ้ นเชิง

---

## 🎯 ตำแหน่งที่ NovaAgent ข่มได ้

> **"OpenCode คือเครื่ องมือ — NovaAgent คือคู่หู"**

| มิติ | OpenCode | NovaAgent (Boss Minimalist) |
|---|---|---|
| **Identity** | Tool เย็นชา, generic | สลี่ — มีตัวตน, มีบุคลิก, เป็ นเพื่อนคู่คิด |
| **Interface** | Terminal + Electron desktop | Browser-first desktop experience (เบากว่ า, realtime) |
| **Memory** | Session ใน SQLite, auto-compact | Self-evolving — เรียนรู้จากบอส, จดจำความชอบ, ปรับตัว |
| **Agency** | build/plan agents + subagent | Multi-agent meeting room + routing อัจฉริยะ |
| **Privacy** | Claim "privacy first" แต่มีข้อยกเว้ น | Local-first, transparent — บอกตรงๆ ว่าอะไรเก็ บอะไรไม่ |
| **Aesthetics** | SaaS template ทั่วไป | Boss Minimalist — dark glassmorphism, ม่วงอ่อน #d5c6e0, neon pulse เขียว |
| **Platform** | macOS/Windows/Linux | Android/Termux-first + browser ทุกระบบ |
| **Cost** | Zen pay-per-request | ใช้ free model routing ที่ทดสอบแล้ว (Groq, OpenRouter) |

---

## ⚔️ กลยุทธ์การออกแบบ (Design Strategy)

### Phase 1 — โจมตีด้วย "ตัวตน" (Identity Strike)
- Homepage ของ NovaAgent ต้องมี "สลี่" เป็ นตัวเอก — ไม่ใช่ product spec
- One CTA: "เริ่มคุยกับสลี่" — ชัดเจน, ไม่แตกทิศ
- แสดง self-evolution capability ชัดเจน — "ยิ่งใช้ ยิ่งรู้จักบอส"

### Phase 2 — โจมตีด้วย "ความจริงใจ" (Radical Transparency)
- หน้ า privacy ที่บอกตรงๆ: อะไรเก็ บ (local), อะไรส่ งออกไป, อะไรไม่เก็ บเด็ดขาด
- เปรียบเทียบกับ OpenCode แบบไม่พาดพิงชื่ อ — "บางเจ้ าบอก privacy first แต่มีข้อยกเว้ น..."

### Phase 3 — โจมตีด้วย "ประสบการณ์" (Experience Superiority)
- Browser-first: เร็วกว่ า, เบากว่ า, realtime เหมือนมีเดสก์ท็อปที่สอง
- Neon pulse ระหว่าง streaming, glassmorphism, caret เขียว — มีชีวิตชีวากว่ า terminal
- Multi-agent room — แสดงภาพ agents ประชุมกัน แทนที่จะเป็ น single chat

### Phase 4 — โจมตีด้วย "ข้อมูล" (Data Counter)
- OpenCode มี /data แสดง model usage
- NovaAgent ควรมี "Evolution Log" — แสดงว่ าสลี่เรียนรู้อะไรจากบอสไปบ้าง (privacy-safe)

---

## ⚠️ สิ่งที่ต้องระวัง (Reality Check)

1. **อย่าประเมินเขาน้อยเกินไป** — 221K stars + 20K commits + engineering discipline สู งมาก
2. **เขาไม่วิ่งตามเรา** — เราต้องสร้างสนามใหม่ (personal AI companion) ไม่วิ่งตาม "coding agent"
3. **Consolation prize** — อย่าออกแบบมาแค่ "สวยกว่ า" แต่ต้อง "ฉลาดกว่ า/รู้จักบอสกว่ า" จริงๆ
4. **Scope ต้องคุม** — OpenCode มี 139 API endpoints; NovaAgent เริ่มจาก core ที่จำเป็นก่อน

---

## 🚦 ขั้นต่อไปที่แนะนำ

1. **Design sprint** — sitemap + wireframe + moodboard NovaAgent web
2. **Lock positioning** — กำหนด messaging หลัก 3 ประโยคให้ชัด
3. **Competitive matrix ละเอียด** — เปรียบเทียบ feature-by-feature กับ Claude Code, Cursor, Windsurf ด้วย

---

*Sources: opencode.ai, opencode.ai/v2/docs, opencode.ai/zen, opencode.ai/data, github.com/anomalyco/opencode, github.com/opencode-ai/opencode (archived)*

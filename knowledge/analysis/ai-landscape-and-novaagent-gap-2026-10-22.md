# AI บ้านอื่นไปถึงไหน และ NovaAgent ต่อยอดอะไรได้ (22 ตุลาคม 2026)

**วันที่เก็บข้อมูล:** 22 ตุลาคม 2026
**วิธีเก็บ:** ค้นคว้าผ่าน sub-agent 3 ด้านขนานกัน (commercial platforms / OSS frameworks / cutting-edge techniques) จากแหล่งปฐมภูมิที่ตรวจสอบได้
**ข้อจำกัด:** ตัวเลข benchmark leaderboard บางตัวดึงไม่ครบ (หน้าเว็บ render ด้วย JS) — ส่วนที่ไม่ยืนยัน ระบุไว้ชัดว่าไม่ยืนยัน

---

## 🏢 1. แพลตฟอร์มเชิงพาณิชย์ — คู่แข่งระดับแนวหน้า

| Agent | สถานะที่ยืนยันได้ (ณ ต.ค. 2026) |
|---|---|
| **Cursor** | ถูก SpaceX เข้าซื้อกิจการ (14 ส.ค. 2026) ใช้โมเดล Grok ของตัวเอง (Grok 4.7 — 21 ก.ย. 2026), มี **Cursor Router** เลือกโมเดลอัตโนมัติ, Cloud Agents, Automations |
| **Devin (Cognition)** | Cloud + Desktop + CLI, spin up VM (Win/Mac/Linux) เพื่อทดสอบในเบราว์เซอร์จริง, **Devin Review** หา bug/vuln, Security Swarm, ระบบ **"Fusion"** สลับโมเดล, **"Memory and dreaming"** (5 ต.ค. 2026) |
| **Claude Code** | Terminal/IDE/Web/iOS/Android/Slack, รันงาน "หลายชั่วโมงถึงหลายวัน", auto mode (7 ส.ค. 2026), self-hosted beta, Projects (รันหลาย agent พร้อมกัน 17 ก.ย. 2026) |
| **Google Antigravity + Jules** | Antigravity = แพลตฟอร์ม agent-first (App/CLI/IDE/SDK) multi-agent parallel + browser-in-the-loop; Jules = async agent บน cloud VM (Ultra 300 tasks/วัน, 60 concurrent) |
| **GitHub Copilot** | cloud agent, รับ 3rd-party agents (Claude Code + Codex), Copilot app เป็น workspace รวมหลาย agent, MCP allowlists |
| **Amazon Q Developer** | ⚠️ AWS จะยุติ support IDE plugins **30 เม.ย. 2027** แนะนำย้ายไป **Kiro** |
| **OpenAI Codex** | ❌ ยังไม่ยืนยัน — เว็บ OpenAI ตอบ 403/404 ทุก path |

**Capability ที่คู่แข่งมีและ NovaAgent ยังขาด:**
- รันงานยาวหลายวัน/หลายชั่วโมงแบบ async (long-horizon supervisor)
- Computer-use ใน VM จริงพร้อม self-test (อัดวิดีโอคลิกทดสอบเอง)
- Multi-agent orchestration + model routing อัตโนมัติ (Cursor Router, Devin Fusion)
- Memory ข้ามงาน (Devin "Memory and dreaming")

---

## 📦 2. Open-Source Frameworks (stars ดึงสดจาก GitHub API 22 ต.ค. 2026)

| ชื่อ | Stars | สถาปัตยกรรมเด่น | ต่อยอดอะไรได้ |
|---|---|---|---|
| **n8n** | 208,269 | Workflow automation, 400+ integrations, MCP client/server | Integration hub + MCP node แบบ plug-in |
| **AutoGPT** | 187,703 | Autonomous loop, low-code block builder | Visual block/graph builder |
| **Dify** | 159,183 | Agentic workflow + RAG + registry รวมศูนย์ | Model+tool registry, tag skills/mcp |
| **Langflow** | 155,898 | Visual graph (React Flow) | UI ออกแบบ flow เอง |
| **MCP Servers** | 91,467 | Canonical MCP reference | สเปคกลางของ skills/tools |
| **OpenHands** (เดิม OpenDevin) | 91,516 | Agent + runtime **sandbox** (Docker), event stream | **Sandboxing pattern** ⭐ |
| **Open Interpreter** | 68,632 | Local code exec, **ACP**, เน้น open models | ACP protocol (ย้ายเป็น Rust) |
| **AutoGen** (microsoft) | 61,518 | Multi-agent conversation | ⚠️ `activeRepoStatus:false` → ดู AG2 |
| **CrewAI** | 59,965 | Role-based crews | **Role-playing team** ตรงกับ NovaAgent ⭐ |
| **Goose** (aaif-goose) | 55,519 | Extensible + MCP + ACP | MCP+ACP+extension ครบ |
| **Aider** | 49,691 | **Repo-map (tree-sitter)** context mgmt, git-native | Repo-map เทคนิค context ที่ขาด ⭐ |
| **LangGraph** | 43,684 | Graph state machine, checkpointing, durable exec | Checkpoint/persistence ข้ามเทิร์น ⭐ |
| **Deep Agents** (langchain) | 30,487 | "Batteries-included harness": planning, sub-agents, **virtual filesystem** | **ตรงกับ NovaAgent มากที่สุด** ⭐ |
| **Smolagents** (HF) | 29,968 | **Code-as-action** (เขียน Python แทน JSON tool calls) | ลด round-trip/ความผิดพลาด tool call |
| **Letta** (เดิม MemGPT) | 25,224 | **Stateful + tiered memory (core/archival/recall)** | Memory architecture ระดับ production ⭐ |
| **Google ADK** | 21,953 | Code-first, multi-agent + **A2A**, eval+deploy | A2A + deployment/eval pipeline |
| **PydanticAI** | 20,775 | Type-safe agent, structured output | Type-safety กับ tool schema |
| **SWE-agent** | 20,608 | Auto-fix issue, **ACI (Agent-Computer Interface)**, sandbox | ACI ออกแบบ interface ให้โมเดลใช้ tool แม่นขึ้น |

**MCP spec ปัจจุบัน = version 2026-07-28** (Hosts/Clients/Servers, JSON-RPC 2.0, features: Resources/Prompts/Tools/Elicitation, extensions: Tasks, Skills over MCP, MCP Apps)

---

## 🔬 3. แนวคิดล้ำสมัย (มี paper/repo อ้างอิง)

| หัวข้อ | แนวคิด | แหล่งอ้างอิง (ตรวจแล้ว) |
|---|---|---|
| Memory | **Dynamic Cheatsheet** — persistent self-curated memory | arXiv:2504.07952 (10 เม.ย. 2025) |
| Memory | **Sleep-time Compute** — คิดล่วงหน้านอกเวลา query ลด test-time compute ~5x | arXiv:2504.13171 (17 เม.ย. 2025) |
| Memory | **GraphRAG** — entity knowledge graph + community summaries | arXiv:2404.16130 (24 เม.ย. 2024) |
| Self-improve | **Reflexion** — verbal RL, สะท้อน feedback เก็บใน episodic memory (HumanEval 91%) | arXiv:2303.11366 (2023) |
| Self-improve | **Darwin Gödel Machine** — agent แก้โค้ดตัวเอง + validate ด้วย benchmark (SWE-bench 20%→50%) | arXiv:2505.22954 (v3 มี.ค. 2026) |
| Multi-agent | **A2A Protocol** — open standard agent↔agent (Google → Linux Foundation, Apache 2.0) | a2a-protocol.org v1.0 |
| Reliability | **OAgents** — agent research ขาด standardization, ผล variance สูง | arXiv:2506.15741 (17 มิ.ย. 2025) |
| Routing | **RouterBench** — benchmark + dataset 405k+ outcomes สำหรับ router | arXiv:2403.12031 (18 มี.ค. 2024) |

**หมายเหตุ:** "episodic/semantic/procedural", "debate/consensus", "blackboard", "guardrails framework" — ยังไม่ยืนยัน paper ต้นทางที่เจาะจง อย่าอ้างว่าเป็นมาตรฐาน

---

## 🎯 ลำดับต่อยอดสำหรับ NovaAgent (เรียงตามความคุ้มค่า)

1. **Eval harness (OAgents)** — ต้องมีก่อน เพราะทุกอย่างอื่นต้องวัดผลได้ (ตอนนี้ยังไม่มี fitness function)
2. **Evolution archive + fitness (DGM)** — เปลี่ยน self-evolution จาก "แก้ตามคำสั่ง" เป็น "พิสูจน์ว่าดีขึ้น"
3. **Sandboxing (OpenHands/SWE-agent)** — แยก execution ออกจาก host สำคัญมากบน Android/Termux
4. **Sleep-time consolidation + Dynamic Cheatsheet** — ใช้เวลาว่าง prerender ความรู้
5. **Learned router (RouterBench)** — แทน rule-based routing
6. **Graph memory (GraphRAG) + A2A** — งานใหญ่ ต้องออกแบบ schema/protocol ก่อน
7. **Repo-map (Aider) + Virtual FS (Deep Agents)** — จัดการ context ให้ฉลาดขึ้น
8. **Type-safe tool schema (PydanticAI)** — ลดปัญหา tool call ผิดพลาด

**เชื่อมโยง:** [AI Beyond Model Limits](ai-beyond-model-limits.md) · [Sally Better Than Ultra Plan](sally-better-than-ultra-plan-2026-10-22.md) · [Astra Infinite Core Next Steps](astra-infinite-core-next-steps-2026-10-22.md) · [GitHub AI Tools Shortlist](github-ai-tools-shortlist-2026-10-22.md) · [Free Model Routing](../analysis/free-model-routing-2026-10.md)

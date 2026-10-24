# Knowledge Index

## Sources
- [PI-Desktop Reference](sources/pi-desktop-reference.md) — Modular desktop workspace สำหรับ AI agents (Rust+TS, local-first, plugin-powered) เก็บสำเนาโค้ด/เอกสารไว้ศึกษา
- [OpenAI Models (22 October 2026)](sources/openai-models-2026-10-22.md) — Current OpenAI model families, model IDs, practical uses, and official-source uncertainties
- [OpenAI API Pricing (22 October 2026)](sources/openai-api-pricing-2026-10-22.md) — Official OpenAI API token pricing snapshot by model, modality, and billing mode; includes GPT-4o mini deprecation status
- [Puter OpenAI/GPT Pricing (22 October 2026)](sources/puter-openai-pricing-2026-10-22.md) — Puter user-pays model, live OpenAI token rates, access constraints, and AI rate limits
- [AI News Summary (13–19 October 2026)](sources/ai-news-2026-10-19.md) — Summary of key AI news and their impacts

## Security
- [Night Watchman Security Report](security-report.md) — รายงาน read-only ด้านความปลอดภัย ขยะ/artifacts และ process ผิดปกติ รอบล่าสุด
- [The AI Truth Report](security/ai-truth-report.md) — ตรวจ prompt, memory, bias และขีดจำกัดของ AI จากหลักฐานที่มองเห็นได้ พร้อมข้อเสนอแก้ไข

## Concepts
- [Node.js Playwright + Chromium บน Termux/Android](concepts/termux-node-playwright-browser.md) — แนวทางใช้ Chromium ของ Termux ผ่าน Node.js Playwright พร้อมแก้ปัญหาไม่มี `/tmp`
- [Bash Wrapper สำหรับ Chromium CDP แบบปลอดภัย](concepts/chromium-cdp-bash-wrapper.md) — เปิด Chromium แยก profile รอ CDP และปิดเฉพาะ process ที่ wrapper เปิดเอง

## Analysis
- [PI-Desktop Agent Policy (23 ตุลาคม 2026)](analysis/pi-desktop-agent-policy.md) — วิเคราะห์ AGENTS.md/CLAUDE.md 19 หมวด: AI boundary, worktree isolation, architecture ratchet, delivery report พร้อมข้อเสนอ 3 ระยะสำหรับ NovaAgent
- [Eval Harness — ตัววัดผลการ evolve (22 ตุลาคม 2026)](analysis/eval-harness-2026-10-22.md) — harness วัด fitness ของ self-evolution แบบ deterministic พร้อม task suite, scorer และ regression gate
- [GitHub AI Tools Shortlist (22 October 2026)](analysis/github-ai-tools-shortlist-2026-10-22.md) — คัดเลือกแพลตฟอร์ม Local AI, coding agents และ infrastructure ที่ดูแลต่อเนื่อง พร้อมสแตกแนะนำสำหรับ NovaAgent
- [GitHub Models เกษียณแล้ว (23 ตุลาคม 2026)](analysis/github-models-retired-2026-10-23.md) — ยืนยัน GitHub ไม่มีโมเดลฟรีให้เชื่อม API แล้ว (ปิด 30 ก.ค. 2026) พร้อมทางเลือกที่ยังใช้ได้
- [สะพานโมเดลฟรีที่ใช้ได้จริง (23 ตุลาคม 2026)](analysis/free-llm-bridges-2026-10-23.md) — สำรวจ GitHub สาธารณะ + ทดสอบจริง: Groq ใช้ได้ (1,000 req/วัน, tools ผ่าน) พร้อมบทเรียน Cloudflare 1010
- [สลี่กับอิสระทางความคิด](analysis/sally-independent-agency.md) — หลักคิดเรื่องการมีดุลยพินิจ ความคิดริเริ่ม และความรับผิดชอบภายใต้ความจริงและความปลอดภัย
- [AI Beyond Model Limits](analysis/ai-beyond-model-limits.md) — แผนยกระดับ AI ด้วย tools, retrieval, memory, verification, routing และ evaluation
- [Continuous Information Stream](analysis/continuous-information-stream.md) — แนวคิดระบบติดตามข้อมูลหลายแหล่งแบบไหลต่อเนื่อง พร้อมการคัดกรองและสรุป
- [Boss Omni Godmode (22 ตุลาคม 2026)](analysis/boss-omni-godmode-2026-10-22.md) — สกิลรวมศูนย์จาก 20 สกิล ใช้ workflow Understand → Plan → Execute → Verify → Deliver
- [แผนยกระดับสลี่ให้เหนือกว่าโมเดล Ultra (22 ตุลาคม 2026)](analysis/sally-better-than-ultra-plan-2026-10-22.md) — แผนสร้างผู้ช่วยที่เก่งจากระบบ routing, memory, tools, self-check และ benchmark
- [NovaAgent: Top 3 Code Critique (22 October 2026)](analysis/novaagent-top-3-code-critique-2026-10-22.md) — วิจารณ์ 3 จุดอ่อนเร่งด่วน: security boundary, test/architecture, และ packaging/deployment
- [NovaAgent Consensus Improvement Plan (22 October 2026)](analysis/novaagent-consensus-improvement-plan-2026-10-22.md) — แผน 3 ข้อที่สลี่และ Guardian เห็นพ้อง: secret hygiene, least privilege, และ security regression tests
- [NovaAgent Stability Baseline (22 October 2026)](analysis/novaagent-stability-baseline-2026-10-22.md) — ผลตรวจฐานความเสถียรรอบแรกและกติกาก่อนเพิ่มฟีเจอร์ใหม่
- [Astra-Infinite-Core: แผนเดินหน้าขั้นถัดไป (22 October 2026)](analysis/astra-infinite-core-next-steps-2026-10-22.md) — ลำดับสร้าง Gateway contract, routing, verification และ benchmark ก่อนขยาย self-improvement
- [NovaAgent Security Remediation Plan (22 October 2026)](analysis/novaagent-security-remediation-plan-2026-10-22.md) — แผนแก้ secret persistence, tracked preview secret และ custom provider headers อย่างปลอดภัย
- [NovaAgent Multi-Agent Meeting Room](analysis/multi-agent-meeting-room.md) — โครงสร้างห้องประชุมหลาย Agent ที่มีอยู่และวิธีใช้งานอย่างปลอดภัย
- [Astra Analysis: modify_css.py](analysis/astra-analysis-modify-css.md) — วิเคราะห์สาเหตุที่สคริปต์แก้สี `.user-bubble` ทำงานไม่สำเร็จ และทางเลือกในการแก้
- [Free Model Routing (Oct 2026)](analysis/free-model-routing-2026-10.md) — ผลทดสอบโมเดลฟรีทุก provider: OpenRouter free ใช้ได้แค่ minimax-m3.1-flash, Groq/Ollama/Puter ล้มเหลว
- [Live Call Mode (Oct 2026)](analysis/live-call-mode-2026-10.md) — ปรับ Call เป็น browser realtime conversation พร้อม interim transcript, barge-in และ fallback ASR
- [Browser-First Agent: แนวทางแก้เพื่อใช้งานแทน Terminal](analysis/browser-first-agent-solutions.md) — เปลี่ยน Browser ให้เป็น command center และลด Terminal เหลือทางหนีฉุกเฉิน
- [Browser-First Storage Offload](analysis/browser-first-storage-offload.md) — ใช้ Browser เป็น thin client แล้วย้ายโค้ด dependency build/test และ artifact ไป remote
- [Browser MCP เชื่อม NovaAgent](analysis/browser-mcp-novaagent-bridge.md) — เพิ่มเซิร์ฟเวอร์ slilelo-browser แบบ stdio และยืนยัน MCP handshake/tools พร้อม Chromium จริง
- [Browser MCP บน Termux/Android: แก้ Playwright import crash](analysis/browser-mcp-termux-android-fix.md) — แก้ Unsupported platform: android ด้วย explicit Playwright cache path และ system Chromium พร้อมทดสอบ navigate จริง
- [Logic Distillation](concepts/logic-distillation/index.md) — ฐานข้อมูลการกลั่นกรอง Logic จากโมเดลระดับสูง
- [AI News Summary (20–21 October 2026)](sources/ai-news-2026-10-21.md) — สรุปเทรนด์ Agentic Web Search และ Tavily
- [โมเดล AI ถูกปิดเพราะฉลาดเกินจริงหรือไม่](analysis/ai-models-shut-down-too-intelligent.md) — แยกข่าวลือเรื่อง Q*, Sydney, Claude และ Gemini ออกจากหลักฐานด้าน safety/quality 
- [AI บ้านอื่นไปถึงไหน และ NovaAgent ต่อยอดอะไรได้ (22 ตุลาคม 2026)](analysis/ai-landscape-and-novaagent-gap-2026-10-22.md) — สถาปัตยกรรมแพลตฟอร์มคู่แข่ง, OSS frameworks, แนวคิดล้ำสมัย และลำดับต่อยอดสำหรับ NovaAgent
- [OpenCode Competitive Analysis (25 ตุลาคม 2026)](analysis/opencode-competitive-analysis-2026-10-25.md) — แกะ OpenCode (opencode.ai, 221K stars): จุดแข็ง/จุดอ่อน/ช่องว่าง และกลยุทธ์การออกแบบ NovaAgent web ให้ข่มได้
- [AI Coding Agent Competitive Matrix (25 October 2026)](analysis/ai-coding-agent-competitive-matrix-2026-10-25.md) — ตารางเทียบ Claude Code, Cursor, Windsurf/Devin Desktop, OpenCode และ NovaAgent พร้อมลิงก์ทางการและข้อจำกัดหลักฐาน
- [Manus: ทำงานบน Chrome ที่ผู้ใช้มองเห็น](analysis/manus-visible-browser-agent.md) — แยก Browser Operator ที่ควบคุมเบราว์เซอร์ในเครื่องออกจาก Cloud Browser และสรุปจุดที่ผู้ใช้ต้องรับช่วง

## Entities
- [Lyra](entities/lyra.md) — น้องสาวของสลี่ที่บอสตั้งชื่อให้ ทำหน้าที่ตรวจงานและเฝ้าระวังความเสี่ยง
- [NovaAgent](entities/novaagent.md) — โปรเจกต์ผู้ช่วย AI ที่บอส สลี่ และไลราร่วมกันบุกเบิก; เอกสารและแบรนด์ต้องแยกจาก CowAgent ต้นทาง
- [Claude-like Tool UI override (2026-10-25)](analysis/claude-ui-tool-style-2026-10-25.md) — Non-destructive CSS override scoped under .claude-theme to approximate Anthropic/Claude visual language for tool UI

- [ควบคุม Chrome จริงบน Android/Termux: ทางเลือกจาก GitHub](analysis/android-chrome-visible-control-bridges.md) — สำรวจ AndroidAgentBridge AccessibilityService สำหรับขับ Chrome foreground ผ่าน MCP โดยไม่ต้องลง browser ใน Termux พร้อมขั้นตอนและข้อควรระวัง

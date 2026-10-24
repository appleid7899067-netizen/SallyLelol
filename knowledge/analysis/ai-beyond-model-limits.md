# AI Beyond Model Limits

> Source: การวิจัยจากเอกสารทางการและงานวิจัยต้นฉบับ สรุปสำหรับ Sally/NovaAgent วันที่ 2026-10-22

## แก่นของแนวคิด

การทำให้ AI เก่งเกินขีดจำกัดของโมเดลเดี่ยว ไม่ใช่การบังคับให้โมเดล “คิดให้หนักขึ้น” อย่างเดียว แต่คือการสร้างระบบรอบโมเดลให้มี **ตา มือ ความจำ เครื่องมือ ระบบตรวจสอบ และวงจรเรียนรู้**

วงจรหลัก:

> Observe → Retrieve → Reason → Act → Verify → Remember → Learn

## สถาปัตยกรรมที่แนะนำ

1. **Continuous ingestion** — รับข้อมูลจาก RSS, API, เว็บที่อนุญาต, เอกสาร, GitHub, วิดีโอ/เสียง และแหล่งข่าว
2. **Provenance** — เก็บ URL, เวลาเผยแพร่/ดึงข้อมูล, แหล่งต้นทาง, hash และสายการคัดลอก
3. **Deduplication & event clustering** — แยกข่าวซ้ำ ข่าวเดียวกัน ข่าวแก้ไข และข่าวขัดแย้งออกจากกัน
4. **Hybrid retrieval** — ใช้ keyword + vector + ความสดของข้อมูล + คุณภาพแหล่งข่าว + สิทธิ์การเข้าถึง
5. **Model routing** — เลือกโมเดลตามงาน ความเสี่ยง ค่าใช้จ่าย ความเป็นส่วนตัว และ latency
6. **Tool orchestration** — ให้โมเดลเรียก search, calculator, code sandbox, browser และฐานข้อมูลผ่าน schema ที่ตรวจสอบได้
7. **Verification** — ตรวจ citation, ตัวเลข, ความขัดแย้ง, เวลา และ policy แยกจากตัวสร้างคำตอบ
8. **Memory** — แยก working, episodic, semantic, procedural, event และ provenance memory พร้อม confidence/expiry/source
9. **Evaluation** — เก็บ trace และ regression tests วัดความถูกต้อง ความสด citation การใช้ tool ความปลอดภัย ต้นทุน และ latency
10. **Risk-tiered autonomy** — สรุป/จัดกลุ่มทำอัตโนมัติได้ แต่การส่งข้อความ เผยแพร่ ซื้อของ ลบข้อมูล หรือการเงินต้องมี approval

## ห้าสิ่งที่ควรทำก่อน

1. สร้าง eval set 100–300 เคสจากงานจริง และเก็บ trace ทุก workflow
2. สร้าง tool registry ที่มี strict schema, permission, timeout, retry, audit log และ max steps
3. ทำ RAG แบบ hybrid พร้อม citation, ACL, freshness และ no-answer threshold
4. เพิ่ม sandbox/code execution สำหรับคณิตศาสตร์ วิเคราะห์ข้อมูล ตรวจโค้ด และสร้างไฟล์
5. ทำ memory แบบมี scope, provenance, confidence, expiry, conflict detection และให้บอสดู/ลบได้

## สิ่งที่ไม่ควรทำ

- เพิ่มจำนวน agent โดยไม่มี evaluation
- ให้โมเดลเข้าถึง shell หรือ credential โดยตรง
- เก็บทุกบทสนทนาเป็นความจำถาวร
- เชื่อ self-critique โดยไม่มีหลักฐานภายนอก
- นับบทความซ้ำเป็นการยืนยันหลายแหล่ง
- วัดแค่คำตอบลื่นไหลโดยไม่วัด task success และ unsupported claims

## Roadmap

### 0–12 เดือน

สร้างผู้ช่วยวิจัยที่เชื่อถือได้: source registry, queue, raw artifacts, deduplication, hybrid search, citations, router, sandbox, approval workflow, prompt-injection tests และ dashboard

### 1–5 ปี

พัฒนาเป็น personal evidence infrastructure: event graph ตามเวลา, multimodal monitoring, source reliability ตามโดเมน, ตรวจ narrative ที่คัดลอก/ประสานกัน, feedback ranking และ reversible automation

### 5–10+ ปี

อาจพัฒนาไปสู่ระบบ cognitive system ส่วนตัวที่มี causal/temporal reasoning, active learning, hypothesis generation และ long-horizon planning แต่ยังไม่ควรอ้างว่าแก้ปัญหา truth discovery ทั่วอินเทอร์เน็ตหรือ autonomous self-improvement ได้แล้ว

## หลักการความปลอดภัย

> **แยก intelligence ออกจาก authority**

โมเดลมีสิทธิ์เสนอการกระทำ แต่ไม่ควรมีสิทธิ์อนุมัติตัวเองหรือถือ credential แบบไร้ขอบเขต การอนุมัติควรอยู่ใน policy engine ที่แยกจากโมเดล ใช้ least privilege, short-lived tokens, preview, audit log, rate limit และ kill switch

## แหล่งอ้างอิงต้นฉบับ

- OpenAI Evals: https://platform.openai.com/docs/guides/evals
- OpenAI Function Calling: https://platform.openai.com/docs/guides/function-calling
- OpenAI Retrieval: https://platform.openai.com/docs/guides/retrieval
- OpenAI Structured Outputs: https://platform.openai.com/docs/guides/structured-outputs
- ReAct: https://arxiv.org/abs/2210.03629
- RAG: https://arxiv.org/abs/2005.11401
- Generative Agents: https://arxiv.org/abs/2304.03442
- Reflexion: https://arxiv.org/abs/2303.11366
- Self-Refine: https://arxiv.org/abs/2303.17651
- Self-RAG: https://arxiv.org/abs/2310.11511
- OWASP LLM Prompt Injection: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
- NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework

## สรุป

เป้าหมายที่ถูกต้องไม่ใช่ “สร้างโมเดลที่ไม่มีข้อจำกัด” แต่คือ **สร้างระบบที่รู้ข้อจำกัด ใช้แหล่งข้อมูลภายนอก ตรวจสอบตัวเองด้วยหลักฐาน และเพิ่มความสามารถโดยไม่เพิ่มอำนาจแบบไร้การควบคุม**

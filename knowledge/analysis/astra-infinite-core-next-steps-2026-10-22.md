# Astra-Infinite-Core: แผนเดินหน้าขั้นถัดไป

> Source: บทสนทนากับบอสและข้อเสนอจาก Lyra, 22 ตุลาคม 2026

## ข้อสรุป

ยังไม่ควรรีบ “รวมโมเดล” เป็นโมเดลเดียว ให้สร้างระบบกลางที่เลือกใช้จุดแข็งของ Astra และ Grok อย่างมีหลักฐานก่อน โดยลำดับที่เหมาะสมคือ **Gateway Contract → Routing → Verification → Benchmark**

## แผน 5 ขั้น

1. **ล็อกสัญญากลางของ Gateway/Bridge**
   - รูปแบบ input/output เดียวกัน
   - timeout, error, cost, privacy และ logging ที่กำหนดชัด
   - แยก provider adapter ออกจาก core เพื่อไม่ให้ core ผูกกับ API ใด API หนึ่ง

2. **ทำ Router รุ่นเล็ก**
   - งานตรรกะ วิเคราะห์ยาว และงานที่ต้องสม่ำเสมอ → Astra
   - งานข้อมูลสดหรือระดมมุมมอง → Grok เฉพาะเมื่อมี live access และหลักฐานรองรับ
   - เริ่มจากเลือกโมเดลหลักทีละงาน ไม่ปล่อยให้ตอบแข่งกันทุกครั้ง

3. **เพิ่ม Verification Layer**
   - ตรวจความสอดคล้อง แหล่งอ้างอิง ความมั่นใจ ความปลอดภัย และข้อมูลลับ
   - หากคำตอบขัดกัน ให้รายงานความขัดแย้งหรือส่งเข้า adjudication ไม่เลือกจากความมั่นใจของโมเดลอย่างเดียว

4. **สร้าง Benchmark ชุดเล็ก**
   - แยกโจทย์ reasoning, สดใหม่, coding, safety และภาษาไทย
   - วัด accuracy, hallucination, latency, cost และ failure rate
   - เก็บ baseline ก่อน แล้วจึงปรับ router/ระบบตรวจคำตอบ

5. **ค่อยเพิ่ม Memory และ Self-improvement**
   - วาง personality, memory และการปรับปรุงไว้หลัง policy boundary
   - ทุกการเปลี่ยน routing หรือระบบต้องมี approval, audit trail และ kill switch
   - ห้าม self-modification หรือเพิ่มสิทธิ์โดยอัตโนมัติ

## ความเสี่ยงที่ต้องคุม

- Grok ไม่ได้แปลว่าสดใหม่เสมอ หากไม่มี retrieval/live access ต้องถือว่ายังไม่ยืนยัน
- การรวมคำตอบอาจเพิ่ม hallucination และสร้างความมั่นใจปลอม
- การส่ง prompt ข้าม provider อาจกระทบความเป็นส่วนตัว ค่าใช้จ่าย และ latency
- Memory/self-improvement แบบไร้ขอบเขตทำให้พฤติกรรม drift และตรวจย้อนกลับไม่ได้

## ความคืบหน้าการลงมือทำ (22 ตุลาคม 2026)

- ตรวจโครงสร้างจริงของ NovaAgent แล้วพบ `bridge/bridge.py`, `bridge/agent_bridge.py`, `models/bot_factory.py` และ provider-specific bots
- สร้างไฟล์เริ่มต้น `models/provider_contract.py` โดยแยก request/response/usage/failure และ capability contract ออกจาก provider implementation
- เพิ่ม `provider_contract_test.py` สำหรับ validation, error category, default capabilities และ latency helper
- ตรวจ syntax และ smoke test ด้วย Python สำเร็จ
- ยังไม่แก้ `bot_factory.py` หรือ `bridge.py` จนกว่า contract จะผ่านชุดทดสอบเต็ม
- การรัน pytest ยังทำไม่ได้ใน environment ปัจจุบัน เพราะไม่มีโมดูล `pytest` ติดตั้ง

## Definition of Ready

เดินหน้าขยายได้เมื่อ Gateway contract และ provider isolation ผ่านการทดสอบ, routing มีเกณฑ์วัดผล, benchmark แสดง baseline, มี timeout/fallback/audit log/secret isolation/kill switch และระบบเปิดเผยคำตอบที่ไม่แน่ใจหรือขัดแย้งตรง ๆ

## Related

- [AI Beyond Model Limits](ai-beyond-model-limits.md) — การยกระดับความสามารถด้วย tools, retrieval, memory และ evaluation
- [NovaAgent Stability Baseline](novaagent-stability-baseline-2026-10-22.md) — กติกาฐานความเสถียรก่อนเพิ่มฟีเจอร์
- [NovaAgent Consensus Improvement Plan](novaagent-consensus-improvement-plan-2026-10-22.md) — secret hygiene, least privilege และ security regression tests

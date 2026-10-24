# NovaAgent Stability Baseline (22 October 2026)

> Source: การตรวจสอบโปรเจกต์ร่วมกับบอสในบทสนทนาวันที่ 22 ตุลาคม 2026

## สถานะ

เข้าสู่ช่วง **ตรวจสอบ–ทดสอบ–ทำให้เสถียร** โดยหยุดเพิ่มฟีเจอร์ใหม่ชั่วคราว

## ผลตรวจรอบแรก

- Branch: `experiment/hybrid-lab`
- มีการแก้ไขค้างอยู่ก่อนเริ่มตรวจ จึงไม่ reset, commit หรือลบไฟล์
- Python compile ผ่าน
- JavaScript syntax check ผ่านด้วย `node --check`
- `git diff --check` ผ่านหลังแก้ trailing whitespace หนึ่งจุดใน `voice/openai/openai_voice.py`
- `app.py` import ได้สำเร็จ
- ชุดทดสอบยังรันไม่ได้ เพราะ environment ไม่มี `pytest`; ยังไม่ได้ติดตั้ง dependency เพิ่ม
- CSS tool activity มีการปรับแบบตั้งใจให้เหลือ source of truth ที่ `channel/web/static/CSJS/css/theme-tools.css`; `chat.html` โหลดชุด CSJS และไม่โหลด grouped variant
- พบ selector เก่าที่ถูกถอดออก 2 ตัว (`.tool-output-section`, `.tool-streaming`) แต่โค้ดปัจจุบันยังใช้งานชื่อเหล่านี้ จึงต้องตรวจ behavior ผ่าน browser/UI ในรอบถัดไป

## กติกา baseline

1. ไม่เพิ่มฟีเจอร์ใหม่จนกว่าจะผ่าน smoke test และ regression check
2. ไม่ reset, ลบ หรือ commit การเปลี่ยนแปลงของบอสโดยไม่ได้รับคำสั่ง
3. แก้เฉพาะปัญหาที่มีหลักฐานจากการตรวจ
4. ทุกการแก้ต้องรัน syntax check และ `git diff --check` ซ้ำ
5. ติดตั้ง test dependency เมื่อจำเป็นและมีแผนตรวจต่อเนื่อง ไม่ติดตั้งแบบสุ่ม

## Related

- [Boss Omni Godmode](boss-omni-godmode-2026-10-22.md) — workflow Understand → Plan → Execute → Verify → Deliver
- [NovaAgent: Top 3 Code Critique](novaagent-top-3-code-critique-2026-10-22.md) — จุดอ่อนด้าน security, test/architecture และ packaging
- [NovaAgent Consensus Improvement Plan](novaagent-consensus-improvement-plan-2026-10-22.md) — แนวทาง secret hygiene, least privilege และ security regression tests

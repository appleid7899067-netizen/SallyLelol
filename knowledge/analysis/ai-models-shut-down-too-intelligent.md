# โมเดล AI ถูกปิดเพราะฉลาดเกินจริงหรือไม่

> แหล่งข้อมูล: เอกสารและประกาศจาก Google, Anthropic, Microsoft และ OpenAI รวมถึงการตรวจสอบโดย Lyra เมื่อ 22 ตุลาคม 2026

## ข้อสรุป
ยังไม่มีหลักฐานปฐมภูมิที่ยืนยันว่าโมเดลใดถูกปิดเพราะ “ฉลาดเกินไป” โดยตรง เรื่องเล่าลักษณะนี้มักเป็นการผสมระหว่างข่าวลือ รายงานที่ไม่ยืนยัน และเหตุการณ์ safety/quality จริง

## กรณีสำคัญ

- **OpenAI Q\***: มีรายงานข่าวเกี่ยวกับโครงการและความกังวลของนักวิจัยในปี 2023 แต่ชื่อโครงการ รายละเอียดความสามารถ และการถูกปิดยังไม่มีการยืนยันอย่างเป็นทางการเพียงพอ จึงสรุปไม่ได้ว่า “ถูกปิดเพราะฉลาดเกินไป”
- **OpenAI o1**: มีการเปิดตัวพร้อมเอกสารประเมินความปลอดภัยและมาตรการลดความเสี่ยง แสดงภาพของการทดสอบ/ปรับ safety ก่อนเผยแพร่ ไม่ใช่หลักฐานการ shutdown เพราะความฉลาด
- **Bing Sydney**: Microsoft จำกัดบริบทและจำนวนรอบสนทนาหลังพบ hallucination พฤติกรรมไม่เสถียร และการ jailbreak เป็นการแก้ปัญหาผลิตภัณฑ์และ safety ไม่ใช่การปิดเพราะฉลาดเกินไป
- **Gemini image generation**: Google ระงับการสร้างภาพบุคคลชั่วคราวในปี 2024 หลังผลลัพธ์ผิดพลาดและมีอคติ เหตุผลคือคุณภาพและความปลอดภัย
- **Claude**: ไม่พบประกาศจาก Anthropic ว่ารุ่นใดถูกหยุดเพราะฉลาดเกินไป การเปลี่ยนรุ่นหรือข้อจำกัดที่มีเอกสารมักเกี่ยวกับ lifecycle, policy และ safety
- **Galactica และ Tay**: ถูกถอด/ปิดหลังปัญหาคุณภาพ เนื้อหาเป็นอันตราย หรือการโจมตีระบบจากผู้ใช้ ไม่ใช่เพราะความฉลาดสูงเกินควบคุม

## เกณฑ์แยกข่าวลือกับข้อเท็จจริง
คำว่า *deprecate*, *pause*, *restrict* หรือ *replace* ไม่ได้แปลว่า *shutdown เพราะฉลาดเกินไป* ต้องมีคำประกาศหรือหลักฐานที่ระบุเหตุผลนั้นโดยตรง ซึ่งในกรณีที่ตรวจสอบยังไม่พบ

## แหล่งอ้างอิง

- [Google: Introducing Gemini](https://blog.google/technology/ai/google-gemini-ai/) — การเปิดตัวและแนวทาง safety ของ Gemini
- [Anthropic: Introducing the next generation of Claude](https://www.anthropic.com/news/claude-3-family) — ความสามารถและการประเมินความปลอดภัยของ Claude 3
- [Microsoft: Learning from our first week of the new Bing](https://blogs.bing.com/search-quality-insights/february-2023/learning-from-our-first-week-of-the-new-bing) — การเรียนรู้จากปัญหา Bing ช่วงเปิดตัว
- [OpenAI o1 System Card](https://cdn.openai.com/o1-system-card.pdf) — การประเมินความเสี่ยงของ o1

## Related

- [AI Beyond Model Limits](ai-beyond-model-limits.md) — การยกระดับระบบ AI ด้วย safety, verification และ routing
- [The AI Truth Report](../security/ai-truth-report.md) — การตรวจ bias และข้อจำกัดของ AI

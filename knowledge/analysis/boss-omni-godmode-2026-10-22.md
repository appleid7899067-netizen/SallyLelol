# Boss Omni Godmode (22 ตุลาคม 2026)

## ข้อสรุป
สร้างสกิลรวมศูนย์ `boss-omni-godmode` เพื่อรวบความสามารถจาก 20 สกิลให้เหลือ workflow เดียว ลดความซ้ำซ้อนและจำนวนสกิลที่ต้องจำ โดยไม่ลบสกิลต้นฉบับ

## ความสามารถหลัก
- Understand: ทำความเข้าใจโจทย์และ definition of done
- Plan: เลือก branch งาน เช่น research, browser/UI, build, debug, design, document และ GitHub
- Execute: ลงมือแบบ defensive ตรวจ input, edge cases และผลกระทบ
- Verify: ตรวจ functional, regression, quality, security, UI และ evidence
- Deliver: รายงานผลลัพธ์ ไฟล์ที่เปลี่ยน หลักฐาน ความเสี่ยง และขั้นถัดไป

## หลักการออกแบบ
ใช้ progressive disclosure: ใส่ workflow ที่จำเป็นในสกิลรวม และเก็บรายละเอียดเฉพาะทางไว้ในสกิลเดิม ไม่โหลดทุก reference ทุกครั้ง สกิลเก่าถูกเก็บไว้เพื่อย้อนกลับหรือใช้เป็นแหล่งอ้างอิง

## ไฟล์
- `skills/boss-omni-godmode/SKILL.md`
- ลงทะเบียนใน `skills/skills_config.json`

## การตรวจสอบ
- ตรวจ frontmatter และหัวข้อ workflow ครบ
- ตรวจ JSON config ด้วย `python -m json.tool`
- สถานะ: ผ่าน

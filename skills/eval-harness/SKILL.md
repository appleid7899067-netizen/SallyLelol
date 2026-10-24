---
name: eval-harness
description: ใช้วัดผล (fitness) ของ self-evolution ว่าดีขึ้นหรือแย่ลงจริง หลังแก้ AGENT.md/MEMORY.md/skills/knowledge ใช้เมื่อ evolve เสร็จแล้วต้องพิสูจน์ว่าไม่ regression ใช้เมื่ออยากเทียบคะแนนก่อน/หลังการเปลี่ยนแปลง
---

# Eval Harness Skill

ตัววัดผลการ evolve ของสลี่ — เปลี่ยนจาก "แก้ตามคำสั่ง" เป็น "พิสูจน์ว่าดีขึ้น"

## เมื่อไหร่ต้องใช้
- หลัง self-evolution เขียนไฟล์ (AGENT.md, MEMORY.md, RULE.md, skills/, knowledge/)
- ก่อน commit การเปลี่ยนแปลงเชิงโครงสร้าง
- เมื่ออยากรู้ว่า fitness ปัจจุบันเป็นเท่าไหร่ เทียบกับ baseline

## วิธีใช้ (3 คำสั่ง)

```bash
# 1) ดูรายงาน + update archive
python3 core/eval/runner.py

# 2) เช็คแบบ gate (exit 1 ถ้า regression) — ใช้ใน hook หลัง evolve
bash core/eval/gate.sh

# 3) ตั้งคะแนนปัจจุบันเป็น baseline ใหม่ (ทำเมื่อมั่นใจว่า improvement จริง)
python3 core/eval/runner.py --accept
```

## หลักคิด
- **Fitness = weighted pass ratio** (0.0–1.0) จาก task suite แบบ deterministic (ไม่เรียก LLM)
- **Regression** = fitness ตกลงจาก baseline → ควรพิจารณา `evolution_undo`
- Harness ที่ไม่สามารถ fail ได้ = ไร้ค่า → ทดสอบด้วยการจำลอง regression เป็นระยะ

## โครงสร้าง
- `core/eval/tasks/*.json` — ชุดโจทย์ + เกณฑ์
- `core/eval/scorers.py` — scorer 8 ชนิด (มี `negate` สำหรับ regex)
- `core/eval/runner.py` — รัน suite, เทียบ baseline, archive
- `core/eval/gate.sh` — regression gate
- `core/eval/baseline.json` — คะแนนอ้างอิง

## การเพิ่ม task ใหม่
สร้างไฟล์ `core/eval/tasks/<id>.json`:
```json
{
  "id": "my-check",
  "category": "general",
  "weight": 2,
  "description": "อธิบายสั้น ๆ",
  "checks": [
    {"type": "contains", "path": "AGENT.md", "value": "สลี่"}
  ]
}
```

## บทเรียน
- `contains` ฟันธงผิดง่าย (คำที่ถูกห้ามอาจปรากฏในบรรทัดที่ห้ามใช้) → ใช้ `regex` + `negate`
- ทุก scorer ต้อง defensive — check ที่พังต้องไม่ทำให้ทั้ง suite พัง

## เชื่อมโยง
- [Eval Harness analysis](../../knowledge/analysis/eval-harness-2026-10-22.md)
- คู่กับกลไก `evolution_undo` (backup_id ใน `memory/evolution/`)

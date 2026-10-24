# Eval Harness — ตัววัดผลการ evolve ของสลี่ (22 ตุลาคม 2026)

## ปัญหาที่แก้
ก่อนหน้านี้ self-evolution ของสลี่ "แก้ตามคำสั่ง" แต่ไม่มีตัวชี้วัดว่าดีขึ้นจริงหรือแย่ลง
ทำให้ไม่รู้ว่าแต่ละการเปลี่ยนแปลงเป็น improvement หรือ regression

## แนวคิด
เปลี่ยนจาก **"แก้ตามคำสั่ง"** → **"พิสูจน์ว่าดีขึ้น"**
รันชุดโจทย์ที่มีเกณฑ์ตรวจชัดเจน (deterministic) ก่อน/หลัง evolve แล้วเทียบคะแนน

## สถาปัตยกรรม
อยู่ที่ `core/eval/` ใน cow workspace:

| ไฟล์ | หน้าที่ |
|---|---|
| `tasks/*.json` | ชุดโจทย์ + เกณฑ์ตรวจ |
| `scorers.py` | ตัวให้คะแนน 8 ชนิด + `negate` |
| `runner.py` | รัน suite → fitness → เทียบ baseline → archive |
| `gate.sh` | hook หลัง evolve: exit 1 ถ้า regression |
| `archive/*.json` | ประวัติคะแนนทุกรอบ |
| `baseline.json` | คะแนนอ้างอิง |

## Fitness
```
fitness = Σ(task_ratio × weight) / Σ(weight)
```
task_ratio = passed_checks / total_checks

## Task suite ปัจจุบัน (baseline 100%)
- **identity** (w=3): AGENT/RULE/USER/MEMORY อยู่ครบ, มี "สลี่"/"Astra", ลงท้ายด้วย "ค่ะ"
- **persona-voice** (w=2): regex negate — ต้องไม่มี "ครับ" ที่ใช้ลงท้าย
- **memory-integrity** (w=3): ไฟล์ความจำมีจริง ไม่รั่ว secret, จำนวนไฟล์ไม่บวมเกิน
- **knowledge-wiki** (w=2): index มี Sources/entities + novaagent.md
- **skills-integrity** (w=3): สกิลแกน 4 ตัว + SKILL.md อ่านได้
- **system-config** (w=2): models.json/package.json parse ได้

## บทเรียนสำคัญ
- Scorer แบบ `contains` ฟันธงผิดได้ง่าย: คำว่า "ครับ" ปรากฏในบรรทัดที่ *ห้ามใช้* จึงต้องใช้
  regex + `negate` แทนการเช็ค substring ตรง ๆ
- Harness ที่ทดสอบตัวเองไม่ได้ = ไร้ค่า จึงต้องจำลอง regression เพื่อพิสูจน์ว่าจับได้จริง
  (ผล: 100% → 86.67% และขึ้น ⚠️ REGRESSION ถูกต้อง)

## เชื่อมโยง
- เป็นรากฐานของ [Evolution archive + fitness (DGM)](../concepts/) และ
  [Learned router](../analysis/) ที่ต้องมีตัววัดก่อน
- ใช้คู่กับกลไก `evolution_undo` (backup_id ใน `memory/evolution/`)

## ขั้นถัดไปที่เกี่ยวข้อง
1. Evolution archive + fitness (รวม DGM-style selection)
2. Sandboxing (Android/Termux)
3. Sleep-time consolidation
4. Learned router
5. Graph memory + A2A

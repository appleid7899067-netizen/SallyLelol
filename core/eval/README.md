# Eval Harness — ตัววัดผลการ evolve ของสลี่

> "แก้ตามคำสั่ง" → "พิสูจน์ว่าดีขึ้น"

## หลักการ

ทุกครั้งที่ self-evolution เปลี่ยนอะไร (AGENT.md, MEMORY.md, skills/, knowledge/)
ระบบจะรัน **suite ของ task ที่มีคะแนนชัดเจน** แล้วเทียบคะแนนก่อน/หลัง
ถ้าคะแนนตกลง → ถือว่า regression → ควร undo

## องค์ประกอบ

| ไฟล์ | หน้าที่ |
|---|---|
| `tasks/*.json` | ชุดโจทย์ + เกณฑ์ตรวจ (deterministic, ไม่ต้องเรียก LLM) |
| `scorers.py` | ตัวให้คะแนนแต่ละเช็ค: `exact`, `contains`, `regex`, `files`, `no_leak` |
| `runner.py` | โหลด task → รัน scorer → รวมเป็น fitness score + เขียน archive |
| `archive/*.json` | ประวัติคะแนนแต่ละรอบ (ใช้เทียบ delta) |
| `baseline.json` | คะแนนอ้างอิงล่าสุด (fitness ปัจจุบัน) |

## Fitness score

```
fitness = Σ(passed_checks) / Σ(total_checks)     # 0.0 – 1.0
```

พร้อมน้ำหนักต่อหมวด (category weight) เพื่อให้งานสำคัญกินคะแนนมากกว่า

## วิธีใช้

```bash
python3 core/eval/runner.py                # รัน suite, เทียบ baseline, อัปเดต archive
python3 core/eval/runner.py --json         # output JSON ล้วน (สำหรับ hook)
python3 core/eval/runner.py --accept       # ยอมรับคะแนนปัจจุบันเป็น baseline ใหม่
python3 core/eval/runner.py --list         # ดู task ทั้งหมด
```

## Hook กับ evolution

หลัง evolution เขียน `memory/evolution/YYYY-MM-DD.md` แล้วรัน:

```bash
python3 core/eval/runner.py --json
```

ค่า `delta` บอกว่าดีขึ้นหรือแย่ลง — ใช้ตัดสินใจว่าจะ `evolution_undo` ไหม

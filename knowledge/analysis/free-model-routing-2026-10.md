# สถานะโมเดลฟรีของระบบ (ทดสอบ 2026-10-20)

## บริบท
ระบบ NovaAgent (~NovaAgent-Clean) ตั้งค่า provider ไว้ 4 รายการใน `config.json` → `custom_providers`:
Puter Bridge (127.0.0.1:8741), Ollama (localhost:11434), Groq (api.groq.com), OpenRouter (api.puter.com)

## ผลทดสอบจริง

| Provider / Model | ผล | สาเหตุ |
|---|---|---|
| OpenRouter `minimax/minimax-m3.1-flash:free` | ✅ ผ่าน ~0.9–1.1s | — |
| OpenRouter โมเดล `:free` อื่น ๆ (nemotron, gemma, lfm, laguna, north-mini-code, dots-3) | ❌ 429 | `free-models-per-day` หมดโควต้า |
| `thinkingmachines/inkling:free` | ❌ 403 | ใช้ได้เฉพาะ agentic harness เท่านั้น |
| `api.puter.com/puterai/openai/v1` | ❌ 401 | token_auth_failed |
| Puter local bridge :8741 | ❌ 500 | เครดิตบัญชีหมด |
| Groq | ❌ 403 | Forbidden |
| Ollama :11434 | ❌ | Connection refused (service ไม่ได้รัน) |

## ข้อสรุป / บทเรียน
- **โมเดลฟรีที่ "ใช้ได้จริง" ตอนนี้มี 1 ตัวเท่านั้น** — `minimax/minimax-m3.1-flash:free`
- OpenRouter จำกัด **50 requests/วัน/key** สำหรับโมเดลฟรี (เพิ่ม 10 credits → 1,000 req/วัน)
- การทดสอบหลายโมเดล "พร้อมกัน" เผาโควต้าเร็วมาก — ควรทดสอบทีละตัวและมี rate limit
- คีย์ OpenRouter ที่ใช้งานได้ 2 ตัว: `custom_api_key`/`open_ai_api_key` (`sk-or-v1-1ad…db844a`) และ `custom_providers[3]` (`sk-or-v1-6d5…435131`)
- **ข้อผิดพลาดที่เจอระหว่างทาง:** `curl -o /tmp/r.json` ล้มเหลวเพราะ Termux ไม่มี `/tmp` (ต้องใช้ `~/cow/tmp`) และ `env_config` ไม่ export key เข้า shell → ต้องอ่าน key จาก `config.json` โดยตรง
- `/usr/bin/time` ไม่มีใน Termux → ใช้ `date +%s%N` แทน

## แนวทางแก้
1. เปิด Ollama local เป็น fallback ที่ไม่ต้องใช้โควต้าอินเทอร์เน็ต
2. เพิ่ม OpenRouter credits 10 ดอลลาร์ → ได้ 1,000 req/วัน
3. ทำ model fallback chain: minimax-free → groq → ollama → puter

**ลิงก์:** [[novaagent-project]]

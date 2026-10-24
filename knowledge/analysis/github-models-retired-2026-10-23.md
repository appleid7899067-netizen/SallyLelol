# GitHub Models เกษียณแล้ว — ไม่มีโมเดลฟรีบน GitHub (23 ตุลาคม 2026)

## สรุป
**GitHub ไม่มีโมเดล AI ฟรีให้เชื่อมแบบ API อีกแล้ว** — บริการ **GitHub Models** ถูกเกษียณถาวรเมื่อ **30 กรกฎาคม 2026** สลี่ตรวจสอบเอง 2 ชั้น (subagent + ยิง endpoint จริง) ผลตรงกัน

## หลักฐาน
- https://docs.github.com/en/github-models → ข้อความตรง: *"GitHub Models has been retired. As of July 30, 2026... The playground, model catalog, inference API, and bring your own key (BYOK) are no longer available to any customer."*
- `https://github.com/marketplace/models` → **HTTP 404**
- หน้า docs ย่อย (`rate-limits`, `using-github-models-with-the-api`) → 404 / เด้งกลับหน้า retired
- `https://models.github.ai/inference/chat/completions` → HTTP 200 + "OK" **แต่เป็นแค่ health/edge response** ไม่ใช่ inference จริง (POST ขอ chat ไม่คืนโมเดล) — **ห้ามตีความเป็นว่าใช้ได้**

## ตารางสถานะ
| ประเด็น | สถานะ |
|---|---|
| GitHub Models | ❌ เกษียณถาวร 30 ก.ค. 2026 |
| marketplace/models | ❌ 404 |
| Inference API | ❌ ปิดให้ลูกค้าทุกคน |
| BYOK | ❌ ยกเลิก |
| Rate limit docs | ❌ 404 |

## ทางเลือกที่ GitHub แนะนำ (ไม่ฟรีแบบเดิม)
- **GitHub Copilot Free** — ฟรีจริง แต่ auto model selection เท่านั้น, 2,000 suggestions/เดือน, ใช้ผ่าน IDE/CLI — **ไม่ใช่ OpenAI-compatible API** → เชื่อมกับ agent ตรง ๆ ไม่ได้
- **Azure AI Foundry** — เสียเงิน (free tier บางส่วน ต้องสมัคร Azure)

## ทางที่ยังใช้ได้จริงสำหรับ NovaAgent
1. **OpenRouter free** — `minimax/minimax-m3.1-flash:free` (ยืนยันใช้ tools ได้) — ดู [Free Model Routing](free-model-routing-2026-10.md)
2. **Gateway 8741** ของบอสเอง (`http://127.0.0.1:8741/v1`)
3. **Local model (Ollama/llama.cpp)** — รอเครื่องใหม่ที่มี RAM/GPU พอ

## บทเรียน
- อย่าเสียเวลาหา "โมเดลฟรีบน GitHub" — มันตายแล้วตั้งแต่กลางปี 2026
- Endpoint ที่ตอบ 200 อาจเป็นแค่ health response — ต้องยิง request จริงและตรวจ payload ถึงจะฟันธงได้

## ลิงก์ที่เกี่ยวข้อง
- [Free Model Routing (Oct 2026)](free-model-routing-2026-10.md)
- [AI Landscape and NovaAgent Gap](ai-landscape-and-novaagent-gap-2026-10-22.md)

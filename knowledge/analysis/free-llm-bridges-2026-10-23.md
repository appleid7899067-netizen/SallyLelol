# สะพานโมเดลฟรีที่ใช้ได้จริง (23 ตุลาคม 2026)

*สำรวจและทดสอบจริงเมื่อ 23 ต.ค. 2026 — หลังพบว่า GitHub Models เกษียณถาวร*

## 🔴 สิ่งที่ "ตายแล้ว" — ห้ามใช้เป็นหลักฐาน

| สิ่ง | สถานะ | หลักฐาน |
|---|---|---|
| **GitHub Models** | ปิดถาวร 30 ก.ค. 2026 | docs ระบุ "has been retired"; marketplace 404 |
| `cheahjs/free-llm-api-resources` | repo 404 | GitHub API ก็ 404 |
| Cerebras free tier | ไม่มีถาวร | docs: "Is there a permanently free tier? No." |
| DeepInfra / Together | ไม่มี free tier | docs ระบุ pay-per-token |
| HuggingFace free chat | credit = 0 | ไม่มี chat ฟรี |
| gpt4free / reverse proxy | ❌ ผิด ToS | เสี่ยง ban — ห้ามใช้ |

## ✅ สะพานที่ใช้ได้จริง (ยืนยันด้วยการยิงจริง)

| อันดับ | Provider | Endpoint | หมายเหตุ |
|---|---|---|---|
| 🥇 | **Groq** | `https://api.groq.com/openai/v1` | ~1,000 req/วัน · tools ผ่าน · เร็วมาก |
| 🥈 | Google Gemini | `generativelanguage.googleapis.com` | context 1M · ไม่ประกาศลิมิตชัด |
| 🥉 | Cloudflare Workers AI | — | 10,000 neurons/วัน |
| 4 | NVIDIA NIM | — | 10,000 req/วัน (ต้องยืนยันเบอร์) |
| 5 | OpenRouter `:free` | `https://openrouter.ai/api/v1` | 50 req/วัน (ต่ำ) |

## 🔑 Groq — รายละเอียดที่ทดสอบแล้ว (23 ต.ค. 2026)

**Endpoint:** `https://api.groq.com/openai/v1` (OpenAI-compatible 100%)

**โมเดลที่ใช้ได้จริง:**

| Model ID | จุดเด่น |
|---|---|
| `openai/gpt-oss-120b` | ใหญ่สุด ฉลาดสุด |
| `openai/gpt-oss-20b` | เร็ว ใช้ tools ผ่าน (ทดสอบแล้ว) |
| `qwen/qwen3.8-27b` | Qwen ใหม่ |
| `allam-2-7b` | เบา |
| `whisper-large-v3-turbo` | เสียง→ข้อความ |

**⚠️ ชื่อโมเดลเก่าใช้ไม่ได้แล้ว:** `llama-3.3-70b-versatile` → `model_not_found`

### 🚨 บทเรียนสำคัญ: Cloudflare error 1010

**Groq อยู่หลัง Cloudflare — บล็อก request ที่ไม่มี User-Agent ปกติ**

| Client | ผล |
|---|---|
| `curl` | ✅ HTTP 200 |
| Python `urllib` (ไม่มี UA) | ❌ HTTP 403 `error code: 1010` |
| Python `urllib` + UA | ✅ HTTP 200 |

**วิธีแก้:** ส่ง header `User-Agent: Mozilla/5.0 ...` ทุกครั้งที่ยิง Groq จาก Python

## 🏠 ทางที่ไม่ต้องพึ่งเน็ต: Local model

- **llama.cpp** — มีคู่มือ Android ทางการ (Termux ใช้ได้)
- โมเดล 1–4B quantized รันไหวบน RAM มือถือ: Qwen2.5-1.5B, Llama-3.2-1B, Gemma-3-1B
- ❌ llamafile ไม่รองรับ Android

## 🔗 ลิงก์ที่เกี่ยวข้อง

- [GitHub Models เกษียณแล้ว](github-models-retired-2026-10-23.md)
- [Free Model Routing (Oct 2026)](free-model-routing-2026-10.md)
- [OpenAI Models](sources/openai-models-2026-10-22.md)

## 🔧 ภาคผนวก: เชื่อม Groq เข้า NovaAgent จริง (23 ต.ค. 2026)

### ชื่อ model vs provider (กับดักสำคัญ)
- `custom_providers` entry `id: groq01` → **provider id** (owned_by)
- **model id ที่ต้องยิง = ค่าฟิลด์ `model` ใน entry** เช่น `openai/gpt-oss-20b`
- ❌ ผิด: `{"model": "custom:groq01"}` → 404 model_not_found
- ✅ ถูก: `{"model": "openai/gpt-oss-20b"}`

### TPM limit ของ Groq ฟรี
- **Limit 8,000 tokens/นาที** (service tier on_demand)
- NovaAgent context default 64k → prompt จริงอาจ 20k+ tokens → **HTTP 413 rate_limit_exceeded**
- Groq ฟรีจึงเหมาะเป็น **fallback** ไม่ใช่โมเดลหลัก
- ยิง Groq ตรงด้วย curl = HTTP 200 (คีย์ใช้ได้จริง)

### path ที่เกี่ยวข้องในโค้ด
- `channel/web/api/openai_compat.py` → `handle_list_models` / `_resolve_model`
- `channel/web/api/sessions.py:506` → `_session_model_catalog()`
- `models/custom_provider.py:47` → `get_custom_providers()` อ่าน `conf().get("custom_providers")`

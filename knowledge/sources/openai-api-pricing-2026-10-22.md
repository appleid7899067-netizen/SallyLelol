# OpenAI API pricing — 22 October 2026

ตรวจสอบเมื่อ: **2026-10-22 (UTC+07)**  
หน่วยราคาในตาราง: **USD ต่อ 1M tokens** (ยกเว้นรายการที่ระบุเป็นต่อนาที/ต่อการเรียก)

## แหล่งข้อมูลทางการและข้อจำกัด

- OpenAI API Pricing: <https://openai.com/api/pricing/> — **เข้าถึงไม่ได้จากสภาพแวดล้อมที่ตรวจสอบ (HTTP 403)** จึงไม่ใช้เป็นแหล่งข้อมูลตัวเลขโดยตรงในรายงานนี้
- OpenAI Developer Docs — Pricing: <https://platform.openai.com/docs/pricing> — เข้าถึงได้ และเป็นแหล่งตัวเลขหลักด้านล่าง
- OpenAI Developer Docs — Models: <https://platform.openai.com/docs/models> — ใช้ยืนยัน model ID และหมวดหมู่โมเดล

ข้อมูลเป็น snapshot ณ วันที่ตรวจสอบ ราคาและความพร้อมใช้งานอาจเปลี่ยนแปลงภายหลัง

## GPT-4o mini (legacy/deprecated)

หน้าโมเดลทางการระบุว่า `gpt-4o-mini` เป็น **Deprecated** แต่ยังแสดงราคาและ alias ที่เกี่ยวข้อง:

| โมเดล | Input | Cached input | Output |
|---|---:|---:|---:|
| `gpt-4o-mini` | $0.15 | $0.075 | $0.60 |

หน่วย: USD ต่อ 1M tokens. หน้าโมเดลระบุว่า alias `gpt-4o-mini` และ snapshot `gpt-4o-mini-2024-07-18` อยู่ในสถานะ Deprecated; ควรตรวจสถานะการใช้งานในบัญชีและวางแผนย้ายไปโมเดลที่รองรับก่อนนำไปใช้ใหม่

## Standard — flagship models

| โมเดล | Input | Cached input | Output | หมายเหตุ |
|---|---:|---:|---:|---|
| `gpt-6-astra` | $10.00 | $1.00 | $50.00 | มีราคา 30m write $12.50 และ 12h write $25.00 |
| `gpt-6.1-sol` | $2.00 | $0.10 | $10.00 | มีราคา 30m write $2.50 และ 12h write $5.00 |
| `gpt-6-luna` | $0.10 | $0.01 | $0.50 | มีราคา 30m write $0.125 และ 12h write $0.25 |

### โหมดอื่นของ flagship models

| โหมด / โมเดล | Input | Cached input | Output |
|---|---:|---:|---:|
| Batch — `gpt-6-astra` | $5.00 | $0.50 | $25.00 |
| Batch — `gpt-6.1-sol` | $1.00 | $0.05 | $5.00 |
| Batch — `gpt-6-luna` | $0.05 | $0.005 | $0.25 |
| Fast — `gpt-6-astra` | $20.00 | $2.00 | $100.00 |
| Fast — `gpt-6.1-sol` | $4.00 | $0.20 | $20.00 |
| Fast — `gpt-6-luna` | $0.20 | $0.02 | $1.00 |
| Ultrafast — `gpt-6-astra` | $60.00 | $6.00 | $300.00 |
| Ultrafast — `gpt-6.1-sol` | $12.00 | $0.60 | $60.00 |

หน้า Pricing ที่ตรวจสอบไม่แสดงแถว Ultrafast ของ `gpt-6-luna` ในผลลัพธ์ที่เข้าถึงได้ จึงไม่รายงานตัวเลขเดาแทน

## Cyber models — Standard

| โมเดล | Input | Cached input | Output | Cache write 30m / 12h |
|---|---:|---:|---:|---:|
| `gpt-5.6-sol` | $4.00 | $0.40 | $20.00 | $5.00 / $10.00 |
| `gpt-5.6-cyber` | $12.50 | $1.25 | $75.00 | $15.625 / $31.25 |

## Life sciences models — Standard

| โมเดล | Input | Cached input | Output |
|---|---:|---:|---:|
| `gpt-rosalind-research` | $5.00 | $0.50 | $25.00 |
| `gpt-rosalind-discovery` | $5.00 | $0.50 | $25.00 |

หมายเหตุจากหน้า Pricing: cache-write pricing ไม่ใช้กับกลุ่มนี้; `gpt-rosalind-research` เริ่มคิดค่าบริการวันที่ 5 October 2026 และการเข้าถึงจำกัดสำหรับองค์กรที่ได้รับอนุมัติผ่าน trusted-access program

## Realtime และ audio generation

| โมเดล | Modality | Input | Cached input | Output / cost |
|---|---|---:|---:|---:|
| `gpt-realtime-2.1` | Audio | $32.00 | $0.40 | $64.00 |
| `gpt-realtime-2.1` | Text | $4.00 | $0.40 | $24.00 |
| `gpt-realtime-2.1` | Image | $5.00 | $0.50 | ไม่คิด output |
| `gpt-realtime-2.1-mini` | Audio | $10.00 | $0.30 | $20.00 |
| `gpt-realtime-2.1-mini` | Text | $0.60 | $0.06 | $2.40 |
| `gpt-realtime-2.1-mini` | Image | $0.80 | $0.08 | ไม่คิด output |

`gpt-live-1` voice session คิด **$0.05/นาที** (ไม่ใช่ token pricing); backend model และ tool usage คิดแยก

## Image generation — Standard

| โมเดล | Modality | Input | Cached input | Output |
|---|---|---:|---:|---:|
| `gpt-image-2.5-sunburst` | Image | $8.00 | $2.00 | $30.00 |
| `gpt-image-2.5-sunburst` | Text | $5.00 | $1.25 | ไม่คิด output |
| `gpt-image-2.5-flare` | Image | $8.00 | $2.00 | $30.00 |
| `gpt-image-2.5-flare` | Text | $5.00 | $1.25 | ไม่คิด output |

Image Batch ที่หน้า Pricing แสดง:

- `gpt-image-2`: Image $4.00 input / $1.00 cached input / $15.00 output; Text $2.50 / $0.625 / ไม่มี output
- `gpt-image-2.5-sunburst`: Image $4.00 / $1.00 / $15.00; Text $2.50 / $0.625 / ไม่มี output
- `gpt-image-2.5-flare`: Image $4.00 / $1.00 / $15.00; Text $2.50 / $0.625 / ไม่มี output

## Specialized models — Standard

| โมเดล | Input | Cached input | Output |
|---|---:|---:|---:|
| `chat-latest` | $5.00 | $0.50 | $30.00 |
| `gpt-5.3-codex` | $1.75 | $0.175 | $14.00 |

Fast pricing for `gpt-5.3-codex`: **$3.50 input / $0.35 cached input / $28.00 output** ต่อ 1M tokens

## Transcription models

รายการต่อไปนี้หน้า Pricing ระบุเป็นต่อนาที ไม่ใช่ราคา token จึงไม่แปลงหรือเดาเป็น USD ต่อ 1M tokens:

- `gpt-realtime-translate`: $0.034/นาที
- `gpt-live-transcribe`: $0.017/นาที
- `gpt-realtime-whisper`: $0.017/นาที
- `gpt-transcribe`: $0.0045/นาที
- `gpt-4o-transcribe`: $2.50 input / $10.00 output ต่อ 1M tokens และประมาณ $0.006/นาที
- `gpt-4o-mini-transcribe`: $1.25 input / $5.00 output ต่อ 1M tokens และประมาณ $0.003/นาที

## เงื่อนไขราคาอื่นที่หน้า official ระบุ

- Regional processing (data residency) endpoints และ FedRAMP endpoints มี uplift 10% สำหรับโมเดลที่เข้าเกณฑ์
- API, Responses, Chat Completions, Realtime, Batch และ Assistants ไม่คิดค่า endpoint แยกต่างหาก; tokens คิดตามอัตราของโมเดลที่เลือก
- Tool usage อาจมีค่าใช้จ่ายแยก เช่น web search $10/1k calls พร้อม search-content tokens ตามอัตราโมเดล, file search storage/tool calls และ containers
- ราคาในรายงานนี้ไม่รวม tool-call, container, file-search, web-search หรือ regional/FedRAMP uplift เว้นแต่ระบุไว้

## สรุปความเชื่อมั่นและข้อจำกัด

ตัวเลขทั้งหมดที่รายงานมาจากหน้า OpenAI Developer Docs — Pricing ที่เข้าถึงได้ ณ วันตรวจสอบ และ model IDs จากหน้า OpenAI Developer Docs — Models ห้ามตีความเป็นราคาคงที่ในอนาคต หน้า `openai.com/api/pricing/` โดยตรงตอบ HTTP 403 ในสภาพแวดล้อมนี้ จึงไม่สามารถยืนยันว่าหน้านั้นมีเนื้อหาเดียวกันแบบเรียลไทม์ได้

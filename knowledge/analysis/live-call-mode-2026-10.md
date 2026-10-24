# Live Call Mode ของ NovaAgent

> Source: การปรับปรุงโปรเจกต์ NovaAgent-Clean ตามบทสนทนากับบอส วันที่ 2026-10-22

## สถานะ

ระบบ Call เดิมเป็นการอัดเสียงเป็นไฟล์แล้วส่ง ASR จากนั้นส่งข้อความเข้าแชทและสร้างเสียง TTS เต็มไฟล์ ระบบเว็บยังไม่มี WebSocket/WebRTC หรือ Realtime Voice โดยตรง

## การปรับปรุงรอบนี้

- แก้ Call frontend ให้รองรับฟิลด์เสียง `audio_url` จาก backend และยังรับ `url` ได้เพื่อความเข้ากันได้
- เพิ่มการวนกลับไปเริ่มฟังอัตโนมัติหลังเสียง AI เล่นจบเมื่อเปิด Auto mode
- ให้ผู้ใช้เริ่มอัดเสียงเพื่อขัดจังหวะเสียง AI ได้
- เมื่อเปิด Auto mode จะเริ่มฟังทันที และเมื่อปิดระหว่างอัดจะหยุดการอัด
- ปรับสี Call จากเขียว/น้ำเงินเป็นโทนม่วงตามแนวทาง Boss Minimalist
- ซิงก์ไฟล์ frontend คู่ `static/` และ `static/CSJS/`
- สำรองไฟล์ก่อนแก้ไว้ใน `tmp/backup/call-live-20261022-023702`

## ข้อจำกัดที่ยังเหลือ

นี่คือ near-realtime turn-based call ไม่ใช่ full-duplex streaming voice: ASR ยังรับไฟล์เต็มก้อน, TTS ยังสร้างเสียงเต็มไฟล์, และการตอบกลับยังอาศัย SSE/DOM flow เดิม หากต้องการประสบการณ์ระดับ Realtime Voice จริง ต้องเพิ่ม streaming ASR/TTS และ WebSocket/WebRTC หรือ Realtime API ในเฟสถัดไป

## การปรับปรุงรอบล่าสุด: Browser realtime conversation

- เพิ่ม `SpeechRecognition`/`webkitSpeechRecognition` แบบ `continuous` และ `interimResults` ใน `call.js` ทั้งสองสำเนา
- แสดง interim transcript สดใน Call modal และส่ง final phrase เข้า chat/SSE ทันทีโดยไม่ต้องอัปโหลดไฟล์เสียงก่อน
- คง MediaRecorder/ASR upload เป็น fallback สำหรับเบราว์เซอร์ที่ไม่รองรับ Speech Recognition
- ค้าง Call lifecycle, รองรับการหยุด/เริ่มฟังใหม่เมื่อ browser ตัด recognition session และรองรับ mute/hangup
- เพิ่ม barge-in: ตรวจพบเสียงพูดแล้วหยุดเสียง AI ทันที
- หยุด recognition ระหว่างส่ง/พูดคำตอบ เพื่อป้องกันไมค์จับเสียง AI วนกลับเข้าระบบ แล้วเปิดฟังต่อหลัง TTS จบ
- ป้องกันการ reset สถานะเป็น idle ก่อน TTS เริ่มเล่นจริง

## การตรวจสอบ

- `node --check` ผ่านสำหรับ Call JavaScript ทั้งสองสำเนา
- `git diff --check` ผ่าน
- สำเนา `call.js` ทั้งสองตำแหน่งตรงกัน

## ข้อจำกัดปัจจุบัน

- Browser Speech Recognition เป็น realtime ที่ฝั่ง client แต่ไม่ใช่ streaming audio ผ่าน WebSocket/WebRTC
- LLM ใช้ SSE streaming ที่มีอยู่แล้ว
- TTS ยังเป็นการสร้างไฟล์เต็มก้อนผ่าน `/api/voice/tts` จึงยังมี latency ก่อนเริ่มพูด
- หากต้องการ full-duplex ระดับโทรศัพท์ ต้องเพิ่ม backend `/api/call` แบบ WebSocket/WebRTC, streaming ASR และ streaming TTS ในเฟสถัดไป

## Related

- [Logic Distillation](../concepts/logic-distillation/index.md) — แนวคิดการแยกและตรวจสอบ logic เป็นชั้น ๆ

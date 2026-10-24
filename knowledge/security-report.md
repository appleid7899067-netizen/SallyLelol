# Night Watchman Security Report

- **สแกนเมื่อ:** 2026-10-22T03:47:56+07:00
- **ขอบเขต:** `/data/data/com.termux/files/home/NovaAgent-Clean` และ process/listener ที่ผู้ใช้ปัจจุบันอ่านได้
- **โหมด:** READ-ONLY; เขียนเฉพาะไฟล์รายงานนี้
- **ข้อจำกัด:** ไม่ใช่ antivirus/forensic proof; process และ network เปลี่ยนแปลงได้ตลอดเวลา; ค่าลับถูก mask

## Executive Summary

- Security findings: **1**
- Junk/artifact findings: **2**
- Process findings: **0**

## Security

### 1. [HIGH] Tracked or repository-local secret-like files
- **หลักฐาน:** `.preview_secret, agent/tools/utils/credentials.py, common/token_bucket.py, docs/ui-starter/design-tokens.md, plugins/banwords/config.json, plugins/godcmd/config.json, plugins/keyword/config.json, skills/claude-api/shared/token-counting.md`
- **ทางเลือก:** Rotate exposed credentials; remove them from history; use environment/secret storage; add CI secret scanning.

## Junk / Artifacts

### 1. [LOW] Generated cache directories
- **หลักฐาน:** `__pycache__=62`
- **ทางเลือก:** Review whether each cache is disposable; add safe paths to ignore rules; remove only after human confirmation.

### 2. [MEDIUM] Backup/swap artifacts
- **หลักฐาน:** `config.json.bak, voice/edge/edge_voice.py.bak2, models/openai/openai_http_client.py.bak, channel/web/static/css/chat.css.bak, channel/web/static/css/base.css.bak, channel/web/static/css/theme-tools.css.bak, channel/web/static/CSJS/css/base.css.bak, channel/web/static/CSJS/css/chat.css.bak, channel/web/static/CSJS/css/theme-tools.css.bak, channel/web/static/CSJS/js/chat/ai-sources.js.bak, channel/web/static/CSJS/js/core/i18n.js.bak2, channel/web/static/js/chat/ai-sources.js.bak, channel/web/static/js/core/i18n.js.bak2`
- **ทางเลือก:** Classify before deletion; move sensitive backups outside the repository; add retention policy and ignore rules.

## Unusual Processes

✅ ไม่พบประเด็นจากการตรวจหมวดนี้ (ไม่ได้แปลว่าปลอดภัยสมบูรณ์)

## วิธีตรวจโดยย่อ

- Git-tracked names, permission metadata, listening sockets (`ss`/`netstat`)
- Cache/backup/large-file inventory โดยไม่อ่านเนื้อหาเพื่อ cleanup
- Process table และ deleted executables ผ่าน `/proc`
- ไม่มีการแก้ระบบ, ลบไฟล์, kill process หรือ rotate secret

## ข้อเสนอแนะรวม

1. ตรวจสอบหลักฐานแต่ละรายการโดยมนุษย์ก่อนดำเนินการ
2. เลือกทางเลือกที่กระทบน้อยที่สุดและทำ backup ก่อนแก้จริง
3. แยก incident response ออกจาก cleanup; อย่าลบหลักฐานก่อนเก็บข้อมูล

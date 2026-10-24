# NovaAgent: Top 3 Code Critique

> Source: ตรวจสอบ repository `~/NovaAgent-Clean` และผลวิเคราะห์แบบ read-only เมื่อ 2026-10-22

## สรุป

จุดอ่อนหลักของ NovaAgent ไม่ใช่จำนวนฟีเจอร์ แต่คือ safety/engineering controls โตไม่ทันอำนาจของระบบ โดย 3 เรื่องเร่งด่วนที่สุดคือ:

1. Security boundary หลอกตัวเอง: full-access เป็นค่าเริ่มต้น และ shell ทำงานบน host ด้วย best-effort parsing
2. Core runtime ใหญ่และ stateful แต่ test coverage ไปกองอยู่ที่ CRUD API เล็ก ๆ
3. Packaging/deployment contract ขัดแย้งกับโค้ดจริง ทำให้ clean install และ production deployment ไม่น่าเชื่อถือ

## หลักฐานสำคัญ

- `agent/permission/policy.py:15-26,45-47` ระบุเองว่า `full-access` คือ no confinement และ checks เป็น argument-level ไม่ใช่ OS sandbox
- `config.json:36,43` มี web password แบบ hard-coded และตั้ง `agent_permission_mode` เป็น `full-access`
- `run_expert.py:7-11` เปิด Expert API ที่ `0.0.0.0:8001`
- `expert_system/api.py:13-19` มี endpoint review ที่ไม่มี auth และคืน `str(e)` ให้ client
- `pyproject.toml:9,18-19` ประกาศ Python `>=3.7` แต่ package discovery include แค่ `cli*`
- `agent/protocol/agent_stream.py`, `agent/memory/conversation_store.py`, `bridge/agent_bridge.py` เป็น hotspots ขนาดใหญ่มาก ขณะที่ test ที่พบส่วนใหญ่มีเพียง `tasks_api/test_app.py`
- `.preview_secret` ถูก track ใน Git และมี credential-like configuration/backups อยู่ใน worktree; `.gitignore` ไม่ใช่การลบ secret ที่เคยรั่ว

## แนวทางแก้ที่ตกลง

### 1. ทำ security boundary ให้เป็นของจริง

- เปลี่ยน default เป็น `read-only` หรือ `workspace-write`
- ใช้ container/bubblewrap/Firejail/ผู้ใช้ OS แยกสำหรับ shell และจำกัด filesystem/network/process
- ลดการใช้ `shell=True`; ใช้ argv/allowlist สำหรับคำสั่งที่ทำได้
- หมุน credential ทั้งหมดที่เคยอยู่ใน tree/backups และเพิ่ม secret scanning
- bind admin service ที่ loopback เป็นค่าเริ่มต้น; public exposure ต้อง explicit + strong secret + HTTPS/reverse proxy
- เพิ่ม auth/rate limit ให้ Expert API และไม่คืน raw exception

### 2. ทดสอบและแยกแกน runtime ที่เสี่ยง

- แยก `agent_stream.py` เป็น turn coordinator, model/retry policy, tool scheduler, cancellation, persistence, event adapter
- ลด singleton/การเข้าถึง private state จาก handler และ inject dependencies
- สร้าง tests สำหรับ permission, auth, path traversal/symlink, subprocess cancellation, SSE disconnect, concurrency, persistence migration, model fallback
- หยุดกลืน `except Exception` แบบกว้างโดยไม่จำแนก error

### 3. ทำ packaging contract ให้ตรงกับของจริง

- เลือก Python baseline จริง; ถ้าใช้ syntax/dep สมัยใหม่ให้ประกาศ `>=3.10` และทำ CI matrix
- แก้ setuptools discovery ให้รวม `agent*`, `channel*`, `bridge*`, `common*`, `models*`, `plugins*`, `voice*`, `translate*` ตามที่ runtime ใช้
- แยก optional dependencies เป็น extras
- มี clean-install smoke test: build wheel → fresh venv → install → import/start health endpoint
- กำหนด startup path เดียวสำหรับ local, Docker และ package

## Related

- [AI News Summary (20–21 October 2026)](../sources/ai-news-2026-10-21.md) — บริบท agentic systems และความเสี่ยงจาก autonomous tooling
- [Logic Distillation](../concepts/logic-distillation/index.md) — แนวคิดการแยก reasoning/logic ออกจาก runtime ที่ซับซ้อน

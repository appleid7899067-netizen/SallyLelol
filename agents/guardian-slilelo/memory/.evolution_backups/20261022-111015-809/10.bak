---
name: night-watchman
description: Read-only system watch for security risks, junk/artifacts, and unusual processes. Produces a masked Markdown report at knowledge/security-report.md and recommendations only; it never changes, deletes, kills, rotates, or fixes anything.
disable-model-invocation: true
---

# Night Watchman

สแกนระบบแบบ **read-only เท่านั้น** แล้วเขียนรายงานลง `knowledge/security-report.md`.

## Hard boundary

Night Watchman มีหน้าที่สังเกตการณ์และรายงาน ไม่ใช่ช่างซ่อม:

- ห้ามแก้ไขหรือลบไฟล์ใด ๆ ยกเว้นเขียน/ทับรายงาน `knowledge/security-report.md`
- ห้าม kill/หยุด/restart process หรือ service
- ห้ามแก้ config, permission, firewall, route, package หรือ environment
- ห้าม rotate, revoke, print หรือส่งต่อ secret
- ห้ามรันคำสั่งที่มี side effect; ใช้เฉพาะการอ่านข้อมูลและการสร้างรายงาน
- ห้ามแสดงค่า token, password, cookie, private key หรือ secret เต็มค่า ให้ mask เสมอ

ถ้าพบสิ่งอันตราย ให้บันทึก **หลักฐานแบบไม่เปิดเผยความลับ**, ระดับความรุนแรง, ผลกระทบ และทางเลือกแก้ไขเท่านั้น

## วิธีใช้งาน

จาก workspace root ให้รัน:

```bash
python skills/night-watchman/night_watchman.py
```

ตัวเลือก:

```bash
python skills/night-watchman/night_watchman.py --project ~/NovaAgent-Clean
python skills/night-watchman/night_watchman.py --output knowledge/security-report.md
```

## ขั้นตอนสแกน

1. ตรวจ root/project path และเวลาเริ่มสแกน
2. ตรวจ security posture: git-tracked secret-like files, plaintext secret indicators, risky permissions, public listeners, exposed services, insecure defaults, world-writable locations
3. ตรวจขยะ/artifacts: logs ใหญ่, cache, `__pycache__`, backup files, core dumps, temporary files, duplicate build artifacts และไฟล์ที่ไม่ควรอยู่ใน repository
4. ตรวจ process: PID/command/user/start time, parent relationship, zombie/orphan signals, deleted executable/cwd, suspicious command patterns และ process ที่ฟังพอร์ต
5. จัดลำดับเป็น Critical/High/Medium/Low พร้อมหลักฐานที่ mask แล้ว
6. เสนอทางเลือกแก้ 2–3 ทางต่อ finding โดยไม่ลงมือทำ
7. เขียนรายงาน Markdown โดยมี timestamp, scope, limitations, findings, recommendations และ clean bill เฉพาะหมวดที่ตรวจแล้วไม่พบประเด็น

## Completion criteria

งานถือว่าเสร็จเมื่อ `knowledge/security-report.md` มีรายงานรอบล่าสุดครบทั้ง 3 หมวด (Security, Junk, Processes), มีรายการคำสั่ง/วิธีตรวจแบบย่อ, ไม่มี secret ค่าเต็ม, และไม่มี action ที่เปลี่ยนแปลงระบบนอกจากการเขียนรายงานนั้นเอง

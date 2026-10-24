# NovaAgent: Consensus Improvement Plan

> Source: การวิเคราะห์ read-only ของ `NovaAgent-Brandable` และการตรวจสอบความเสี่ยงโดย Guardian Slilelo เมื่อ 2026-10-22
>
> ขอบเขตสำคัญ: รายงาน Night Watchman เดิมสแกน `NovaAgent-Clean` ไม่ใช่ `NovaAgent-Brandable` จึงใช้เป็นสัญญาณเตือนและต้อง revalidate กับ checkout เป้าหมายก่อน remediation

## ข้อสรุป

สลี่และ Guardian Slilelo เห็นพ้องกันใน 3 แผนที่มีผลกระทบสูงและปลอดภัยในหลักการ หากทำตาม safeguards และ acceptance gates ด้านล่าง:

1. Secret and artifact hygiene
2. Least-privilege permission and tool boundary
3. Security regression tests and runtime decomposition

Guardian ไม่อนุมัติให้เริ่ม deployment/reproducibility เป็นแผนเดี่ยวก่อน เพราะต้องจัดการ secret, permission และ API exposure ให้แน่นก่อน

## แผนที่ 1: Secret และ artifact hygiene

### เหตุผล
ผลสแกนเดิมพบ secret-like files ระดับ HIGH และ backup artifacts ระดับ MEDIUM ขณะที่โค้ดมี configuration สำหรับ credential ของหลาย provider และมีการส่งค่า API key เข้า environment ของ subprocess บางส่วน

### งานที่เสนอ

- สแกน working tree และ Git history ของ `NovaAgent-Brandable` โดย mask ค่า secret
- จำแนกทุก finding ว่าเป็น credential จริงหรือ synthetic/example
- Rotate credential ใด ๆ ที่เคยถูกเปิดเผย ก่อนลบหรือ rewrite history
- เก็บ runtime secret ใน environment หรือ secret store ไม่ใช่ tracked config/backup
- เพิ่ม CI/pre-commit secret scanning และ block ไฟล์ backup/swap ที่ไม่ควร track
- ตรวจว่า logs, tool output, prompts, archives และ generated backups ไม่พิมพ์ secret

### เงื่อนไขความปลอดภัยจาก Guardian

- ต้องเก็บหลักฐานก่อน cleanup และห้ามลบ backup แบบเหมา
- ห้ามพิมพ์ token เต็มในรายงานหรือ CI output
- ต้องมีขั้นตอน false-positive สำหรับเอกสารตัวอย่าง
- ห้ามถือว่า `.gitignore` แก้ secret ที่เคย track หรืออยู่ใน history แล้ว

### Acceptance criteria

- Current tree และตัวอย่าง Git-history scan ไม่พบ high-confidence secret ที่ยังใช้งานได้
- Credential ที่อาจรั่วถูก rotate หรือมีหลักฐานว่าเป็น synthetic
- CI ล้มเหลวเมื่อใส่ test secret และเมื่อเพิ่ม backup artifact ที่ไม่อนุญาต
- ระบบเริ่มทำงานได้ด้วย sanitized config และ external secret source

## แผนที่ 2: Least-privilege permission และ tool boundary

### เหตุผล
โค้ดระบุว่า `full-access` ไม่มี confinement จริง และ shell path ใช้ `shell=True`; default ที่กว้างเกินไปเพิ่ม blast radius ของ prompt injection, tool misuse และ delegated agents

### งานที่เสนอ

- ให้ installation ใหม่เริ่มที่ `read-only` หรือ `workspace-write`
- ให้ `full-access` เป็น explicit opt-in พร้อม warning และ audit trail
- บังคับ authentication/authorization ก่อนแก้ permission mode ผ่าน web API
- ตรวจ policy ให้ครอบคลุม foreground/background shell, browser, MCP, scheduler, file operations และ subagents
- ทำ canonical path และ symlink escape checks
- บังคับให้ delegation/subagent ลดสิทธิ์ได้ แต่เพิ่มสิทธิ์เหนือ parent ไม่ได้
- ปฏิเสธการ bind service ภายนอก loopback หากไม่มี strong auth/token
- สำหรับ hostile หรือ multi-tenant deployment ใช้ OS/container sandbox จริง เพราะ policy layer ไม่ใช่ sandbox สมบูรณ์

### เงื่อนไขความปลอดภัยจาก Guardian

- read-only ห้าม write/delete/config change/side-effect tool
- workspace-write ห้ามหลุด workspace ผ่าน symlink, relative path, archive หรือ child process
- background job ต้องใช้ policy เดียวกับ foreground
- remote/untrusted deployment ห้ามได้ `full-access` โดยปริยาย
- การเปลี่ยน default ต้องมี compatibility path สำหรับ deployment เดิมที่ opt-in อย่างชัดเจน

### Acceptance criteria

- Fresh config bind loopback และไม่เลือก `full-access` โดยอัตโนมัติ
- Unsafe host/password/token combinations ถูก reject หรือปิดใช้งานแบบ fail-closed
- Unauthorized UI/API requests ได้ `401/403`; valid auth ใช้งานได้
- Tests ยืนยัน permission narrowing, path/symlink protection และ policy parity ของ background jobs

## แผนที่ 3: Security regression tests และแยก runtime ที่เสี่ยง

### เหตุผล
runtime หลักมี stateful hotspots ขนาดใหญ่ ขณะที่ test coverage ที่ค้นพบยังไม่ครอบคลุม permission, auth, subprocess, delegation และ persistence อย่างเพียงพอ การเพิ่ม tests เป็นการลดความเสี่ยงโดยไม่เพิ่ม authority ให้ระบบ

### งานที่เสนอ

- สร้าง isolated test suite ด้วย temporary directories และ fake credentials
- เพิ่ม negative tests สำหรับ permission, path traversal/symlink, secret redaction, auth, subprocess timeout/cancellation, MCP environment filtering และ delegation narrowing
- ทดสอบว่า Expert API ไม่คืน raw exception หรือข้อมูลภายใน
- แยกแกนใน runtime เช่น turn coordinator, model/retry policy, tool scheduler, cancellation, persistence และ event adapter โดยเริ่มจาก seam ที่ทดสอบได้ง่าย
- ลด broad exception swallowing และจำแนก error ให้ชัด
- แยก network/integration tests และปิดเป็นค่าเริ่มต้นใน CI

### เงื่อนไขความปลอดภัยจาก Guardian

- Tests ห้ามใช้ credential จริง, production endpoint หรือไฟล์ production
- Fixture ห้ามแตะ `config.json`, databases, memory หรือ credential files จริง
- Security tests ต้องเป็น release gates ไม่ใช่แค่รายงาน warning
- ต้องคง positive control เช่น `ast.literal_eval` และทดสอบไม่ให้ parser ย้อนกลับไปใช้ `eval`

### Acceptance criteria

- CI รันจาก clean checkout ได้โดยไม่ต้องมี real API key
- มี regression tests ครอบคลุม permission, secret redaction, auth, path safety และ subprocess/delegation
- Tests deterministic และไม่แก้ production state
- การละเมิด permission/auth หรือ package/runtime import สำคัญทำให้ release fail

## ลำดับดำเนินงานที่เห็นพ้อง

1. Re-scan และจำแนก/rotate secret ของ `NovaAgent-Brandable` ก่อน cleanup
2. ลด default authority และปิดช่อง permission/tool boundary
3. เพิ่ม regression gates เพื่อพิสูจน์ว่า boundary ยังอยู่
4. หลังจากนั้นจึงยกระดับ deployment/reproducibility: pin image/dependencies, non-root, read-only filesystem, secret injection, API auth และ egress controls

## Guardian verdict

ทั้ง 3 แผนได้รับสถานะ **Approve with safeguards** ไม่ใช่การอนุญาตให้แก้ไฟล์ทันที Guardian ตรวจสอบความเสี่ยงและรายงานเท่านั้น ไม่ได้ execute, write, edit, delete หรือเปลี่ยน configuration ใด ๆ

## Related

- [Night Watchman Security Report](../security-report.md) — ผลสแกน read-only ล่าสุดและข้อจำกัดด้านขอบเขต
- [NovaAgent: Top 3 Code Critique](novaagent-top-3-code-critique-2026-10-22.md) — การวิเคราะห์จุดอ่อนด้าน security boundary, test/architecture และ packaging

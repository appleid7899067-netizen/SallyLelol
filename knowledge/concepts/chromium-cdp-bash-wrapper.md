# Bash Wrapper สำหรับ Chromium CDP แบบปลอดภัย

> Source: แนวทางจากบทสนทนาและการติดตั้งจริงใน `~/NovaAgent-Clean` เมื่อ 2026-10-25

แนวทางใช้ Bash wrapper เปิด Chromium Headless แบบชั่วคราวสำหรับงาน Puppeteer/Playwright โดยสร้าง profile แยก, รอ CDP พร้อม, รันคำสั่งโปรเจกต์ และปิดเฉพาะ process ที่ wrapper เปิดเอง

## Key Points

- ใช้ `scripts/with-chromium.sh` ใน NovaAgent-Clean
- ค่าเริ่มต้นใช้ `chromium-browser`, CDP bind ที่ `127.0.0.1:9222` และ profile ชั่วคราวใต้ `$TMPDIR`
- wrapper รองรับ `BROWSER`, `CDP_HOST`, `CDP_PORT` และ `STARTUP_TIMEOUT`
- ตรวจ `/json/version` ก่อนเริ่ม เพื่อป้องกันการไปแตะ Chromium/CDP instance ที่มีอยู่แล้ว
- ใช้ `trap cleanup EXIT INT TERM` เพื่อ cleanup เมื่อคำสั่งจบหรือกด Ctrl+C
- ห้ามใช้ `pkill chromium` เพราะอาจปิด Browser ตัวอื่น
- Puppeteer เชื่อมด้วย `puppeteer.connect({ browserURL: "http://127.0.0.1:9222" })`
- Playwright เชื่อมด้วย `chromium.connectOverCDP("http://127.0.0.1:9222")`

## Verification

ทดสอบจริงใน NovaAgent-Clean:

1. ใช้ `bash -n scripts/with-chromium.sh`
2. ใช้ `CDP_PORT=9223 ./scripts/with-chromium.sh node test-puppeteer.js`
3. Puppeteer เปิด `https://example.com`, อ่าน title/body ได้ และ wrapper ปิด Chromium หลังจบ
4. ไม่พบ profile wrapper ค้างหลังจบ
5. เมื่อ `9222` มี CDP อยู่แล้ว wrapper ยกเลิกด้วย exit code 1 โดยไม่แตะ instance เดิม
6. `npm install --package-lock-only --ignore-scripts --no-audit --no-fund` สำเร็จ

## Related

- [Node.js Playwright + Chromium บน Termux/Android](termux-node-playwright-browser.md) — การตั้งค่า Chromium และ temporary directories บน Termux
- [NovaAgent](../entities/novaagent.md) — โปรเจกต์ที่ใช้ wrapper นี้

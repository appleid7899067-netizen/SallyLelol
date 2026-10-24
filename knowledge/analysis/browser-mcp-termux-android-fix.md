# Browser MCP บน Termux/Android: แก้ Playwright import crash

> Source: การตรวจสอบและทดสอบจริงใน NovaAgent เมื่อ 24 ตุลาคม 2026

## อาการ

NovaAgent hot-reload พบ `slilelo-browser` แล้ว แต่ MCP handshake ล้มเหลวด้วย:

```text
Error: Unsupported platform: android
at computeDefaultCacheDirectory (.../playwright-core/...)
```

สาเหตุเกิดก่อน `chromium.launch()` เพราะ Playwright คำนวณ default browser cache ตอน import module และไม่รองรับ `process.platform === "android"` ในจุดนั้น

## วิธีแก้

ใน `browser-mcp-server/src/browser.js`:

1. ย้ายการ import Playwright จาก static import เป็น dynamic import
2. กำหนด `PLAYWRIGHT_BROWSERS_PATH` เป็นโฟลเดอร์ภายใน server ก่อน import
3. ใช้ Chromium ของ Termux ผ่าน `executablePath` ที่ resolve จาก candidate paths อยู่แล้ว

การแก้แบบนี้ไม่ดาวน์โหลด browser เพิ่ม และยังคงใช้ system Chromium เดิม

## ผลตรวจสอบ

- MCP `initialize` ผ่าน
- `tools/list` ผ่านและพบ 14 tools
- เรียก `navigate` ไป `https://example.com` ผ่าน HTTP 200
- ได้ snapshot ของหน้าเว็บและ interactive ref กลับมา
- `mcp.json` เหลือ server เดียวคือ `slilelo-browser` เพื่อลดความสับสนกับ `@playwright/mcp` เดิม

## ข้อควรระวัง

การตรวจตรงของ MCP server ผ่านแล้ว แต่ควรตรวจ log ของ NovaAgent หลังข้อความถัดไปเพื่อยืนยันว่า hot-reload นำ server เวอร์ชันแก้ไขกลับเข้า ToolManager สำเร็จ หากยังเห็น handshake error เก่า ให้ restart NovaAgent หนึ่งครั้ง

## Related

- [Browser MCP เชื่อม NovaAgent](browser-mcp-novaagent-bridge.md) — การเชื่อมต่อ MCP และ protocol handshake
- [Browser-First Agent](browser-first-agent-solutions.md) — แนวทางใช้ Browser เป็น command center

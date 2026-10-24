# ใช้ Node.js Playwright + Chromium บน Termux/Android

## สรุป
บน Termux/Android การติดตั้ง Python Playwright อาจไม่มี wheel ที่ตรงกับแพลตฟอร์ม โดยเฉพาะเมื่อใช้ Python รุ่นใหม่และ `aarch64` แต่ Node.js Playwright สามารถใช้ร่วมกับ Chromium ที่ติดตั้งผ่านแพ็กเกจ Termux ได้

## สาเหตุที่ค้นพบ
- Python Playwright `1.52.0` ไม่มี distribution ที่ใช้ได้กับ Termux/Android + Python 3.14 + aarch64
- ระบบมี Chromium ของ Termux อยู่แล้วที่ `/data/data/com.termux/files/usr/lib/chromium/chrome`
- ระบบมี Node.js Playwright ใน `browser-mcp-server/node_modules`
- MCP subprocess ล้มเหลวเพราะ Chromium พยายามใช้ `/tmp` แต่ Termux ไม่มี `/tmp`

## วิธีแก้
ก่อน import/launch Playwright ให้ตรวจ Termux แล้วตั้ง temporary directories ไปยัง `$PREFIX/tmp`:

```js
const termuxTmp = join(process.env.PREFIX || '/data/data/com.termux/files/usr', 'tmp');
mkdirSync(termuxTmp, { recursive: true });
process.env.TMPDIR ||= termuxTmp;
process.env.TMP ||= termuxTmp;
process.env.TEMP ||= termuxTmp;
```

จากนั้นใช้ `executablePath` ชี้ไปยัง Chromium ของ Termux และ launch ด้วย flags ที่เหมาะกับ Android เช่น `--no-sandbox` และ `--disable-dev-shm-usage`

## Verification
- Direct `BrowserSession` เปิด `https://example.com` ได้และอ่าน title/text ได้
- MCP client เรียก `tools/list` ได้ 14 tools
- MCP `navigate` ไป `https://example.com` ได้ HTTP 200 และคืน snapshot สำเร็จ โดยทดสอบในสภาพแวดล้อมที่ลบ `TMPDIR`, `TMP`, `TEMP` ออกแล้ว เพื่อยืนยันว่าโค้ดตั้งค่าเองจริง

## ข้อจำกัด
- เส้นทางนี้ใช้ Node.js Browser MCP ไม่ใช่ Python browser service เดิม
- ต้องให้ NovaAgent เชื่อม MCP server `slilelo-browser` ผ่าน stdio ตาม `mcp.json`
- ไม่ควรติดตั้ง Python Playwright ซ้ำบน Termux เว้นแต่แพลตฟอร์ม/เวอร์ชัน Python เปลี่ยนและมี wheel รองรับ

## อ้างอิง
- [NovaAgent](../entities/novaagent.md)
- [Browser-First Agent Solutions](../analysis/browser-first-agent-solutions.md)

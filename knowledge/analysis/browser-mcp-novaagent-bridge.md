# Browser MCP เชื่อม NovaAgent

> Source: การตรวจสอบและลงมือเชื่อมระบบใน workspace เมื่อ 24 ตุลาคม 2026

## สรุป

เลือกใช้ Browser MCP ฝั่ง Node ที่มีอยู่แล้วเป็น backend หลัก แทนการรื้อ BrowserTool ฝั่ง Python ซึ่ง environment ปัจจุบันยังไม่มีแพ็กเกจ Python Playwright แต่ระบบ Node มี Playwright และใช้ Chromium ของ Termux ได้จริง

## สิ่งที่ทำ

- เพิ่ม server `slilelo-browser` ใน `mcp.json` แบบ stdio
- ชี้ไปยัง `/data/data/com.termux/files/home/cow/browser-mcp-server/src/index.js`
- คง server `playwright` เดิมไว้เป็นทางเลือกสำรอง
- ใช้ `browser-cli.mjs` เป็น one-shot wrapper สำหรับงาน shell และ smoke test

## หลักฐานการตรวจสอบ

- `node browser-cli.mjs self-test https://example.com` ผ่าน: HTTP 200, ดึงข้อความได้ 917 ตัวอักษร และสร้าง screenshot ได้
- MCP JSON-RPC handshake ผ่าน
- `tools/list` ผ่าน และประกาศเครื่องมือ 13 รายการ ได้แก่ navigate, snapshot, click, fill, select, press, screenshot, get_text, evaluate, wait, scroll, back, forward และ close
- `mcp.json` ผ่าน JSON validation

## ข้อจำกัด

- ยังไม่ได้เปลี่ยน BrowserTool Python ให้ไปใช้ Node MCP โดยตรง เพราะ NovaAgent มี MCP client อยู่แล้วและการเชื่อมผ่าน `mcp.json` เป็น seam ที่เล็กกว่าและปลอดภัยกว่า
- การทดสอบผ่าน NovaAgent process เต็มรูปแบบยังไม่ได้รัน เนื่องจากคำสั่งทดสอบที่เรียก `shutdown()` ถูก safety guard ระงับ; การทดสอบ protocol ระดับ process ทำแทนแล้ว
- `browser-cli.mjs` เปิด browser ใหม่ต่อคำสั่ง แต่เก็บ URL ล่าสุดไว้ ส่วน MCP server จะคง browser session ตลอดอายุ process

## Related

- [NovaAgent](../entities/novaagent.md) — โปรเจกต์ปลายทางที่รับ MCP server
- [Browser-First Agent](browser-first-agent-solutions.md) — แนวคิดใช้ Browser เป็น command center
- [Browser-First Storage Offload](browser-first-storage-offload.md) — การแยกภาระ browser/client ออกจาก runtime หลัก

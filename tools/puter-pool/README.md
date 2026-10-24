# Puter Pool — สลับบัญชี Puter อัตโนมัติ

รวม token หลายบัญชี Puter แล้วสลับอัตโนมัติเมื่อบัญชีหนึ่งหมดเครดิต/โดน limit

## วิธีใช้

### 1. เพิ่ม token (บอสทำเอง — ห้ามส่งในแชท)

สร้างไฟล์ `tokens.json` ในโฟลเดอร์นี้:

```json
{
  "accounts": [
    { "name": "acc1", "token": "eyJhbGciOi...", "note": "บัญชีหลัก" },
    { "name": "acc2", "token": "eyJhbGciOi...", "note": "" }
  ]
}
```

แล้วตั้งสิทธิ์:
```bash
chmod 600 tokens.json
```

### 2. เช็คสถานะทุกบัญชี
```bash
node pool.js health
```

### 3. เรียกใช้งาน
```bash
node pool.js chat "สวัสดี"           # ถามสั้น ๆ
node pool.js chat --model gpt-5.4 "..." # เลือกโมเดล
```

### 4. ผ่าน CLI หลัก
```bash
sally "ช่วยเช็คดิสก์"
sally -i
```

## กลไกสลับบัญชี

```
ยิงบัญชีที่ 1 → 200 OK → ใช้ผล
              → 429/402/unavailable → ลองบัญชีถัดไปทันที
              → ทุกตัวพัง → รายงาน error ชัดเจน
```

## ความปลอดภัย

- `tokens.json` ถูก chmod 600 (เจ้าของเท่านั้น)
- **ห้าม commit** `tokens.json` ขึ้น git
- token ที่โพสต์ในแชทถือว่ารั่ว → ควร revoke แล้วออกใหม่

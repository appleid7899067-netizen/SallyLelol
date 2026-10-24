# Browser-First Storage Offload

> Source: ข้อสรุปจากการสนทนากับบอส วันที่ 22 ตุลาคม 2026

## หลักการ

Browser ไม่สามารถแทนพื้นที่เก็บข้อมูลได้ทั้งหมด แต่สามารถเป็นหน้าควบคุมของสถาปัตยกรรม **Thin Browser + Remote Workspace** ได้ โดยย้ายโค้ด dependency การ build/test และ artifact ขนาดใหญ่ไปไว้บน remote/cloud แล้วให้เครื่องท้องถิ่นเก็บเพียง browser profile, config, cache ขั้นต่ำ และไฟล์ที่กำลังใช้งาน

## แนวทาง

- ใช้ GitHub/GitLab เป็นที่เก็บโค้ด
- ใช้ remote server หรือ Cloud IDE สำหรับ build/test
- ใช้ cloud storage สำหรับไฟล์ขนาดใหญ่
- ดู log และผลลัพธ์ผ่าน Browser แบบ streaming แทนการดาวน์โหลด
- เก็บ screenshot/log เฉพาะหลักฐานสำคัญ พร้อม expiration
- ล้าง cache, temp และ artifact อัตโนมัติตามอายุ
- ดาวน์โหลดเฉพาะไฟล์ที่ต้องใช้จริง

## ข้อจำกัด

Browser ยังใช้พื้นที่สำหรับ cache, profile, session data และไฟล์ชั่วคราว จึงไม่ใช่การกำจัดพื้นที่ทั้งหมด เป้าหมายคือทำให้เครื่องเป็น thin client และย้ายภาระหนักออกไปนอกเครื่อง

## สถาปัตยกรรม

```text
User → Browser Dashboard → Remote Workspace / Cloud API
                                  ├─ code
                                  ├─ build/test
                                  ├─ logs
                                  └─ artifacts
```

## Related

- [Browser-First Agent](browser-first-agent-solutions.md) — แนวคิดใช้ Browser เป็น command center

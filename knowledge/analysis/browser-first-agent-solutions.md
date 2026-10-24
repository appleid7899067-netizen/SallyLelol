# Browser-First Agent: แนวทางแก้เพื่อใช้งานแทน Terminal

> Source: การระดมแนวคิดจากบทสนทนากับบอส วันที่ 22 ตุลาคม 2026

## แก่นของปัญหา

การใช้ Terminal มากทำให้บอสต้องคิดเป็นคำสั่งและรายละเอียดเชิงเทคนิคเอง ขณะที่เป้าหมายจริงคือให้ Agent รับเจตนา แล้วลงมือทำผ่านเครื่องมือที่มองเห็นและตรวจสอบได้ จึงควรออกแบบระบบแบบ **Browser-first, Terminal-minimal**

## ทางออกหลัก

### 1. Browser Command Center
สร้างหน้าเดียวที่รวมแท็บ งานที่กำลังทำ สถานะการล็อกอิน screenshot และผลลัพธ์ ให้ Browser เป็น dashboard กลางของ Agent แทนการสลับคำสั่งใน Terminal

### 2. Intent-to-Action Layer
บอสพิมพ์เจตนา เช่น “เช็กหน้าเว็บนี้ว่ามีปุ่มเสียไหม” แล้วระบบแปลงเป็น workflow อัตโนมัติ: เปิด URL → สำรวจ DOM/ARIA → คลิกเส้นทางสำคัญ → ตรวจ console/network → สรุปผล

### 3. Browser-native Workspace
ใช้หน้าเว็บหรือ local web app เป็นพื้นที่ทำงาน: แก้ config แบบฟอร์ม, ดูไฟล์ผลลัพธ์, ปรับ task, ดู diff และกดยืนยัน แทนการให้บอสพิมพ์คำสั่งเอง

### 4. Reusable Browser Recipes
บันทึกงานที่ทำซ้ำเป็นสูตร เช่น login → เปิด dashboard → export report หรือเปิดเว็บ → กรอกข้อมูล → screenshot → สรุปผล แล้วเรียกใช้ด้วยภาษาธรรมชาติ

### 5. Visual Verification Loop
ทุกงานที่แก้ UI ต้องมีหลักฐานอัตโนมัติ: screenshot ก่อน/หลัง, ขนาด viewport หลายแบบ, ตรวจ overflow/clipping/contrast และรายงานจุดผิดปกติ

### 6. Safe Approval Gates
งานเสี่ยง เช่น ส่งข้อความ ลบข้อมูล เผยแพร่ หรือจ่ายเงิน ต้องหยุดที่หน้าอนุมัติพร้อม preview สิ่งที่จะเกิดขึ้น ให้บอสกดอนุมัติครั้งเดียว ไม่ต้องใช้ Terminal

### 7. Browser Memory
จำ session, เว็บไซต์ที่ใช้บ่อย, selector ที่เสถียร, ขั้นตอนที่สำเร็จ และข้อผิดพลาดเดิม โดยไม่เก็บรหัสผ่านหรือ secret ลงในข้อความธรรมดา

### 8. Self-healing Selectors
เมื่อ selector เดิมพัง ระบบใช้ role, label, text, DOM proximity และ screenshot ช่วยหาองค์ประกอบใหม่ แล้วรายงานว่าซ่อมเส้นทางให้แล้ว ไม่ล้มเพราะ CSS เปลี่ยนเล็กน้อย

### 9. Multi-agent Browser Review
ให้ Agent หลักทำงานผ่าน Browser และให้ Lyra ตรวจเฉพาะความเสี่ยง: ขอบเขตสิทธิ์, URL ผิด, การส่งข้อมูล, การกระทำถาวร และหลักฐานก่อนรายงานผล

### 10. Terminal Escape Hatch
ไม่ต้องกำจัด Terminal ทั้งหมด แต่ซ่อนไว้เป็นทางหนีฉุกเฉิน ใช้เฉพาะเมื่อ Browser ทำไม่ได้จริง พร้อมบอกเหตุผลและคำสั่งที่กำลังจะรันให้เห็นก่อน

## ลำดับการทำที่แนะนำ

1. เริ่มจาก Browser Command Center + Visual Verification
2. เพิ่ม Intent-to-Action และ Reusable Recipes
3. เพิ่ม Approval Gates และ Browser Memory
4. เพิ่ม Self-healing Selectors
5. ปิดท้ายด้วย Multi-agent Review และ Terminal Escape Hatch

## เกณฑ์วัดว่าเหนือกว่า OpenCode จริง

- งานเว็บทั่วไปสำเร็จโดยไม่ต้องเปิด Terminal
- ทุกการกระทำสำคัญมีหลักฐาน screenshot/log
- งานซ้ำเรียกใช้ด้วยประโยคเดียว
- เมื่อ selector เปลี่ยน ระบบกู้ workflow ได้
- งานเสี่ยงไม่เกิดโดยไม่มีการอนุมัติ
- บอสเห็นสถานะและผลลัพธ์ได้จากหน้าเดียว

## Related

- [Live Call Mode](../analysis/live-call-mode-2026-10.md) — แนวคิดการทำงานแบบโต้ตอบแบบเรียลไทม์
- [NovaAgent Stability Baseline](../analysis/novaagent-stability-baseline-2026-10-22.md) — หลักการตรวจสอบก่อนเพิ่มความสามารถ

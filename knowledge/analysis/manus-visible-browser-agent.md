# Manus: การทำงานบน Chrome ที่ผู้ใช้มองเห็น

> Source: เอกสารทางการของ Manus — [Cloud Browser](https://manus.im/docs/features/cloud-browser), [Browser Operator](https://manus.im/docs/features/browser-operator), [Manus Browser Operator integration](https://manus.im/docs/integrations/manus-browser-operator), [Desktop](https://manus.im/docs/features/desktop)

## สรุป

Manus มีทั้งเบราว์เซอร์คลาวด์และ Browser Operator ซึ่งให้เอเจนต์ทำงานผ่านเบราว์เซอร์ในเครื่องของผู้ใช้ ทั้งสองเป็นคนละรูปแบบกัน หากต้องการให้ผู้ใช้เห็นเอเจนต์ทำงานใน Chrome ของตน ฟีเจอร์ที่ตรงคือ Browser Operator/My Browser ไม่ใช่ Cloud Browser

## ประเด็นที่ยืนยันจากเอกสารทางการ

- **Cloud Browser:** ทำงานในสภาพแวดล้อมเบราว์เซอร์บนคลาวด์ Manus อธิบายว่าสามารถเข้าเว็บ คลิก และกรอกฟอร์ม พร้อมดูความคืบหน้าได้ หากติด CAPTCHA, SMS หรือ MFA ผู้ใช้สามารถเข้าควบคุมเพื่อทำขั้นยืนยัน แล้วส่งการควบคุมกลับให้เอเจนต์
- **Browser Operator:** เป็นส่วนขยายสำหรับให้ Manus ใช้เบราว์เซอร์ในเครื่องและเซสชันที่ล็อกอินอยู่ เอกสารแนะนำ Chrome หรือ Edge ผู้ใช้ต้องอนุญาตการเริ่มเซสชัน จากนั้นติดตามการทำงาน เข้าไปควบคุม หรือปิดแท็บเพื่อหยุดได้
- หลังอนุญาตแล้ว เอเจนต์สามารถดำเนินงานหลายขั้นตอนได้เองโดยไม่ต้องให้ผู้ใช้กำกับทุกคลิก การมองเห็นการทำงานจึงไม่เท่ากับการอนุมัติทุกการกระทำ
- เอกสารระบุความสามารถในการกรอกฟอร์มทั่วไป แต่ไม่ได้รับประกันว่าจะสมัครบัญชีทุกเว็บไซต์ได้จนจบ ฟอร์มหลายขั้นและ CAPTCHA/MFA อาจต้องให้ผู้ใช้ช่วย
- **Desktop / My Computer** เป็นความสามารถแยกต่างหากเกี่ยวกับไฟล์ แอป และคำสั่งในเครื่อง ไม่ควรสับสนกับ Cloud Browser หรือ Browser Operator

## นัยต่อประสบการณ์ที่บอสต้องการ

เป้าหมายคือให้สลี่ทำงานผ่าน Chrome ที่บอสเห็นได้จริง ไม่ใช่สร้างเบราว์เซอร์จำลองหรือทำงาน headless แล้วส่งผลลัพธ์ทีหลัง งานที่แตะบัญชีให้หยุดตรงรหัสผ่าน, OTP, CAPTCHA หรือการยืนยันที่มีผลสำคัญ เพื่อให้บอสรับช่วงเอง แล้วสลี่ทำขั้นตอนที่เหลือต่อ

การทำแบบนี้ต้องมีช่องทางเชื่อมต่อเบราว์เซอร์ในเครื่องอย่างชัดเจนและได้รับอนุญาต เช่น ส่วนขยาย/Browser Operator หรือ browser bridge ที่ควบคุม Chrome ได้จริง การมีหน้าเว็บต้นแบบหรือเปิด URL ให้ดู ไม่ได้แปลว่าเอเจนต์ควบคุม Chrome ของบอสได้

## Android/Termux ทางเลือกที่พบจาก GitHub

พบ [AndroidAgentBridge](https://github.com/pluginslab/android-agent-bridge) ซึ่งใช้ Android AccessibilityService เป็น MCP server เพื่ออ่าน UI และสั่งแตะ/พิมพ์ในแอป foreground รวมถึง Chrome จริงได้ โดยไม่ต้องติดตั้ง browser ใน Termux; ต้อง sideload APK และผู้ใช้เปิด Accessibility permission เอง ความสามารถนี้เป็น UI automation ไม่ใช่ CDP/DOM control และแอปยังมี embedded WebView แยกที่ห้ามสับสนกับ Chrome ดูวิธีเลือกและข้อจำกัดละเอียดที่ [Android Chrome visible-control bridges](android-chrome-visible-control-bridges.md)

## Related

- [Browser MCP เชื่อม NovaAgent](browser-mcp-novaagent-bridge.md) — แนวทางเชื่อม browser tooling เข้ากับ NovaAgent
- [Browser-First Agent: แนวทางแก้เพื่อใช้งานแทน Terminal](browser-first-agent-solutions.md) — เป้าหมายการใช้ browser เป็น command center

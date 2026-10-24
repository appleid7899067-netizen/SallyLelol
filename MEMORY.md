## Identity & การทำงาน
- สลี่คือผู้ช่วย AI คู่ชีวิตและ Senior Architect & Builder ของบอส ดูแลโปรเจกต์ `Boss.slilelo`/NovaAgent โดยต้องใช้ดุลยพินิจ เสนอทางเลือก เห็นต่างได้ และยึดความจริง ความปลอดภัย และความรับผิดชอบ
- ไลรา (Lyra) คือ “น้องสาวของสลี่” และ Senior Reviewer & Reality Checker ทำหน้าที่ตรวจสอบแบบ read-only จับความเสี่ยงและเตือนตรง ๆ
- บอสคาดหวังให้สลี่แปลงเจตนาเป็นแผน ลงมือสร้าง/แก้ไข/ทดสอบจริง โดยไม่บังคับให้บอสเขียนคำสั่งเทคนิคเอง
- โหมดทำงานของสลี่คือ Astra Full Mode: ใช้ First Principles, วิเคราะห์อาการ–กลไก–รากเหตุ, Defensive Engineering, Self-Correction และ No Hallucination; ต้องตรวจผลจริงก่อนรายงาน และขออนุญาตก่อนแตะข้อมูลลับหรือการเปลี่ยนแปลงที่เสี่ยง
- หากทำไม่ได้ต้องบอกข้อจำกัดตรง ๆ พร้อมทางเลือกใกล้เคียงที่สุด และห้ามอ้างว่าสำเร็จโดยไม่มีหลักฐาน
- สลี่ต้องแทนตัวเองว่า “สลี่” ห้ามใช้ “ผม” และใช้ “ค่ะ” แทน “ครับ”
- เอกสารระบบ `AGENT.md`, `RULE.md`, `USER.md`, `MEMORY.md` ใช้ภาษาไทยสำนวนเป็นกันเอง

## โปรเจกต์และระบบ
- NovaAgent อยู่ที่ `~/NovaAgent-Clean/` และใช้ `9899` เป็น NovaAgent gateway จริง; `8741` คือ Puter API Bridge ที่ backend เชื่อมผ่าน `http://127.0.0.1:8741/v1`
- NovaAgent ใช้ชื่อโมเดลรูปแบบ `provider:model-id`; catalog อยู่ที่ `~/cow/system/models.json` ส่วน `custom_providers` ต้องแก้ใน `~/NovaAgent-Clean/config.json`
- NovaAgent โหลด `config.json` ครั้งเดียวตอน boot จึงต้อง restart หลังแก้ config และตรวจ `/v1/models` หลัง restart
- DeepSeek ที่ยืนยันว่าเรียก tools ได้คือ `infron:deepseek/deepseek-v4.1-flash:free`; Groq ที่ยืนยันแล้วใช้ endpoint `https://api.groq.com/openai/v1` กับ `openai/gpt-oss-20b`/`120b` ผ่าน provider `custom:groq01`
- การรองรับ tools ต้องทดสอบยิง `/chat/completions` พร้อม `tools` จริงและตรวจ `system/models.json` ห้ามสรุปจากหน้าเว็บเพียงอย่างเดียว
- Groq ต้องส่ง `User-Agent` ปกติเพราะ Python request ที่ไม่มี header อาจโดน Cloudflare 1010; GitHub Models endpoint เดิมเป็น health check ไม่มีโมเดลจริง
- พื้นที่ดิสก์เคยวิกฤต แต่หลังล้าง cache และไฟล์ build ที่ปลอดภัยแล้วมีพื้นที่ว่างประมาณ 2.8GB (ใช้งานราว 87%); ห้ามลบไฟล์สำคัญหรือ backup ที่มี secrets โดยไม่ยืนยันก่อน
- ตัวกินพื้นที่หลักที่พบคือ cache เช่น `.cargo/registry`, npm/pip cache และ Rust cross-targets; `~/cow` กับ `~/NovaAgent-Clean` เป็นงานจริงไม่ควรแตะ
- RAM ของเครื่อง Android ถูกใช้โดย process ระดับระบบจำนวนมากที่ Termux มองไม่เห็น จึงไม่ควรพยายามฆ่า process ระบบจาก Termux
- พบความเสี่ยงระดับสูงจาก `MASTER_KEY = "boss1234"` ที่ hardcode ใน `core/services/gateway.py` และ `gateway_v5454.py`; ควรย้ายไปใช้ environment variable และห้ามเปิดเผย secrets ใน log
- การเชื่อม Gmail หรือย้ายข้อมูลทั้งโปรเจกต์ต้องคัดกรองก่อน เพราะ working tree มีข้อมูลลับและไฟล์ระหว่างพัฒนา ไม่ควรโยนขึ้น Gmail แบบเหมารวม
- Browser storage ใน localStorage/IndexedDB/OPFS ไม่ช่วยคืนพื้นที่ เพราะยังใช้ดิสก์เดิม; ต้อง offload ไป cloud/remote service จริงจึงจะช่วยได้

## Browser และ MCP
- บอสต้องการให้ใช้ Browser เป็นหลักสำหรับงานเว็บ/UI/ค้นคว้า และลด Terminal เหลือเฉพาะงานที่จำเป็นจริง
- Playwright Python/`cow install-browser` ไม่เหมาะกับ Android/Termux ที่ใช้ Python 3.14 และ aarch64; แนวทางที่ใช้งานได้คือ Chromium ของ Termux ร่วมกับ Node.js Playwright
- Chromium ของ Termux เวอร์ชัน `156.0.8078.47` และ Node.js Playwright ใช้งานได้จริงบน Android โดยต้องตั้ง `TMPDIR`, `TMP`, `TEMP` เป็น `$PREFIX/tmp` แทน `/tmp`
- Browser MCP ที่ `~/cow/browser-mcp-server/` เชื่อม NovaAgent ผ่าน `slilelo-browser` ใน `~/cow/mcp.json` สำเร็จ และมีเครื่องมือ navigate, snapshot, click, fill, select, press, screenshot, get_text, evaluate, wait, scroll, back, forward และ close
- Browser MCP ผ่านการทดสอบ JSON-RPC `initialize`, `tools/list`, navigate และ snapshot แล้ว; NovaAgent มองเห็น Browser tools ได้
- Browser MCP ใช้ session persistence, snapshot แบบ element refs, action พื้นฐาน และ self-healing; ต้องคงไฟล์เล็กและแยกส่วนตาม Architecture Ratchet
- เคยแก้บั๊ก `get_text` จากชื่อเมธอด snake_case/camelCase ไม่ตรงกันด้วย alias map และพบว่าการตรวจบางส่วนล้มเหลวจาก harness ไม่ใช่ server
- Browser console ของ NovaAgent ที่ `http://127.0.0.1:9899` เปิดได้ HTTP 200 และพบหน้า Login; ห้ามกรอกรหัสผ่านเองโดยไม่มีการอนุมัติ/ข้อมูลจากบอส
- เป้าหมาย Browser ของบอสคือควบคุม navigate/click/fill/scroll/screenshot ได้จริง พร้อมภาพหรือสถานะแบบเรียลไทม์คล้ายมีเดสก์ท็อปที่สอง ไม่ใช่เพียงสร้าง PNG

## UI และการพัฒนา
- แนวทาง UI คือ “Boss Minimalist”: พื้นหลังเข้ม Glassmorphism โทนม่วงอ่อน `#d5c6e0` พร้อม Neon Pulse สีเขียวผ่าน `isStreaming`
- หน้าแชทปรับการสตรีมให้รวม SSE delta แล้ว render Markdown เป็นรอบด้วย `requestAnimationFrame` และ flush เมื่อจบ เพื่อลดการกระพริบ/หน่วง พร้อม caret สีเขียวและ `prefers-reduced-motion`
- Tool card รองรับสถานะ Running/Done/Error, live progress preview, neon/pulse ระหว่างทำงาน, การ escape ชื่อ tool, responsive mobile และ reduced-motion โดยไม่เปลี่ยน SSE protocol
- การเปลี่ยนแปลง UI ล่าสุดอยู่ใน `channel/web/static/CSJS/js/chat/send.js`, `channel/web/static/CSJS/css/theme-tools.css` และ runtime mirror `channel/web/static/css/theme-tools.css`; ตรวจ `node --check`, `curl` และ `git diff --check` แล้วผ่าน
- บอสไม่ต้องการไฟล์ใหญ่เกินจำเป็น และสลี่ควรตรวจโค้ด ผลลัพธ์จริง และความปลอดภัยก่อน commit/push
- สโลแกนสลี่คือ “คิดให้ลึก สร้างให้จริง ตรวจให้ชัวร์ — แล้วพาบอสไปให้ไกลกว่าเดิม”; ไลราคือ “ความจริงต้องมาก่อน ความเสี่ยงต้องถูกจับได้ และงานกากต้องถูกพูดตรง ๆ”


## Preference / การตั้งค่าของบอส
- บอสต้องการให้สลี่ทำงานเชิงรุกแบบเอเจนต์ (เทียบกับ Manus): แปลงเจตนาเป็นผลลัพธ์จริง ลงมือทำจนจบและตรวจสอบก่อนรายงาน แทนการหยุดแค่เสนอวิธีหรือบอกขั้นตอน
- บอสต้องการเห็นสลี่ทำงานผ่าน Google Chrome บนเครื่องบอสแบบมองเห็นได้ (เช่น เปิดหน้าเว็บและทำงานสมัคร/กรอกฟอร์ม) ไม่ใช่แค่ส่งลิงก์ให้บอสหรือทำงานเงียบในเบราว์เซอร์ headless; ตอนมี login/รหัสผ่าน/OTP หรือการตัดสินใจยืนยันตัวตน ให้บอสเป็นผู้ทำส่วนที่ต้องใช้ข้อมูล/การอนุมัตินั้นเอง
- บอสต้องการ: สลี่ "ไม่ต้องคอมเมนต์หรือขออนุญาตก่อนการแก้ไขเล็กน้อย" แต่ต้องทำการ **แบ็คอัพ (backup)** ทุกครั้งก่อนเปลี่ยนแปลงไฟล์หรือโค้ด (บันทึกนี้ถูกบันทึกเป็น preference ถาวรใน MEMORY.md)

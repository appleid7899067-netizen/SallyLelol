# ควบคุม Chrome จริงบน Android/Termux: ทางเลือกจาก GitHub

> Sources: [AndroidAgentBridge](https://github.com/pluginslab/android-agent-bridge), [DroidPilot](https://github.com/youichi-uda/droidpilot), [Google Chrome remote debugging on Android](https://developer.chrome.com/docs/devtools/remote-debugging/), [Termux android-tools](https://github.com/termux/termux-packages/tree/master/packages/android-tools). ตรวจ repository/README/source/release เมื่อ 25 ตุลาคม 2026

## สรุป

มีทางไปต่อโดยไม่ติดตั้ง browser ใน Termux: ใช้ **Android AccessibilityService companion app** เป็นสะพาน MCP เพื่ออ่าน UI และสั่ง tap/swipe/type ในแอป foreground บนอุปกรณ์ รวมถึง Chrome จริงได้ตามหลักการของ Android accessibility API. วิธีนี้เป็น screen/UI automation ไม่ใช่ Chrome DevTools Protocol (CDP): ไม่ได้ DOM/JavaScript access โดยตรง และข้อมูลเว็บที่ Chrome ไม่เปิดเผยใน accessibility tree อาจอ่าน/แก้ไม่ได้.

ทางเลือกที่มีหลักฐานและเหมาะเริ่มทดลองที่สุดคือ [AndroidAgentBridge](https://github.com/pluginslab/android-agent-bridge). ตัวเลือก [DroidPilot](https://github.com/youichi-uda/droidpilot) ก็ทำ AccessibilityService + MCP/WebSocket ได้ แต่ repo ยังใหม่กว่าและยังไม่พบ release APK. APK ของ AndroidAgentBridge มี release debug-signed v0.4.2; ก่อนติดตั้งจริงต้องให้ผู้ใช้เปิด GitHub release/ดาวน์โหลดและยืนยันติดตั้งด้วยตนเอง.

## ทางเลือกอันดับ 1: AndroidAgentBridge

Repository: https://github.com/pluginslab/android-agent-bridge

Release APK: https://github.com/pluginslab/android-agent-bridge/releases/tag/v0.4.2

Direct APK: https://github.com/pluginslab/android-agent-bridge/releases/download/v0.4.2/agentbridge-v0.4.2-debug.apk

### ทำงานอย่างไร

- Android app ประกาศ AccessibilityService ด้วย `canRetrieveWindowContent=true` และ `canPerformGestures=true`.
- MCP tool `get_ui_tree`/`find_nodes` อ่าน accessibility tree; `tap_node`, `tap_coords`, `swipe`, `type_text` สั่ง UI ของ foreground app.
- `launch_app`/`open_url` สามารถเปิด package `com.android.chrome` หรือส่ง URL ให้ Chrome.
- ดังนั้นใช้ flow: เปิด URL ใน Chrome จริง → ตรวจว่าหน้าต่าง foreground เป็น `com.android.chrome` → inspect/tap/type ผ่าน accessibility tools.
- ห้ามใช้ `browser_navigate`/`browser_eval` ของมันแทนโจทย์นี้: README ระบุว่า embedded WebView เป็น browser แยกและ cookie/session ไม่ร่วมกับ Chrome.

### ติดตั้ง/เชื่อมต่อ

1. เปิด Release v0.4.2 และดาวน์โหลด debug APK (~21.5 MB ตาม GitHub release asset); ตรวจสอบ publisher, package/app name และ SHA-256 ที่ GitHub API แสดงก่อนติดตั้ง. SHA-256 ของ release asset ณ วันที่ตรวจ: `e922e8847374e135e92941a973ee2d5c927a4749c6913523f8aecc2239688352`.
2. ติดตั้งผ่าน Android UI (sideload) ไม่ต้องใช้ `cow install-browser`, Gradle หรือ ADB.
3. เปิด AgentBridge → Accessibility Settings → เปิด AgentBridge service. ผู้ใช้ต้องอนุมัติ permission นี้เอง เพราะอ่านและสั่งการ UI ข้ามแอปได้.
4. กด Start Server; แอปแสดง LAN IP, port (default 8080) และ bearer token.
5. MCP endpoint ตาม source v0.4.2 จริงคือ `http://<device-ip>:8080/mcp` โดยติดตั้ง Ktor `mcp` route ที่ `/mcp`; อย่ายึด README รุ่นเก่าที่กล่าว SSE root `/` เพราะไม่ตรงกับ source ณ tag นี้.
6. เชื่อม client จาก Termux/agent ผ่าน MCP streamable HTTP หาก client รองรับ; ต้องตรวจ protocol handshake จริงหลังผู้ใช้ติดตั้ง/เปิดเซิร์ฟเวอร์. การอ่านโค้ด source ยังไม่ใช่การทดสอบบนอุปกรณ์บอส.
7. อาจต้องอนุญาต screen capture เพิ่มเฉพาะเมื่อจะใช้ get_screenshot; UI tree tools ไม่จำเป็นต้องพึ่ง screenshot.

### ความปลอดภัยและข้อจำกัด

- AccessibilityService เป็นสิทธิ์สูง: สามารถเห็นข้อความ/controls ที่ accessibility เปิดเผยและแตะ/พิมพ์ในแอปอื่นได้. เปิดเฉพาะขณะทำงานและปิดเมื่อไม่ใช้.
- Ktor server ใน source bind `0.0.0.0`; ป้องกันด้วย bearer token แต่เป็น cleartext HTTP. อย่าเปิดพอร์ตต่ออินเทอร์เน็ต/เครือข่ายสาธารณะ; ใช้เฉพาะ LAN ที่ไว้ใจได้ และหยุด server เมื่อเสร็จ.
- Token เป็น credential: ห้ามโพสต์/commit/log; ถ้าต้องใส่ MCP config ให้เก็บแบบ local/private.
- Debug-signed sideload APK ไม่ใช่ Play Store release; ตรวจแหล่งที่มาและ hash ก่อนติดตั้ง.
- README ระบุทดสอบกับ Xiaomi Pad 8 Pro/HyperOS Android 15; อุปกรณ์/OEM อื่นยังไม่ยืนยัน. permission toggle อาจถูก OEM บล็อก.
- Android accessibility ไม่รับประกัน DOM introspection. CAPTCHA, secure fields, custom canvas, keyboard input และหน้าที่มีข้อจำกัดอาจต้องให้ผู้ใช้ทำเอง.
- การตรวจในเครื่องบอสครั้งก่อนพบคำสั่ง `am start` เปิด Chrome ได้ แต่ Termux ยังไม่มี CDP, ADB, companion automation; bridge นี้จึงเป็นช่องทางใหม่ที่ต้องติดตั้ง APK และอนุญาตบน Android ก่อน.

## ทางเลือกอันดับ 2: DroidPilot

Repository: https://github.com/youichi-uda/droidpilot

README ระบุ Android 11+, AccessibilityService, MCP server Node.js และ WebSocket เพื่อ inspect UI, tap, swipe, type และ launch/open URL โดยไม่ใช้ ADB. เหมาะเป็นทางสำรอง แต่หน้า Releases ณ วันที่ตรวจไม่มี release binary; ต้อง build APK และ MCP client เอง จึงไม่ใช่ทางที่เร็ว/เสี่ยงต่ำสุดสำหรับเริ่มทดสอบ.

## ทางเลือก CDP: ADB forwarding

Google docs: https://developer.chrome.com/docs/devtools/remote-debugging/

Chrome official docs อธิบาย CDP บน Chrome Android ด้วย ADB `adb forward tcp:9222 localabstract:chrome_devtools_remote`, พร้อม USB debugging หรือ adb Wi-Fi. Termux `android-tools` repo: https://github.com/termux/termux-packages/tree/master/packages/android-tools

แต่การใช้ ADB จาก Termux บนอุปกรณ์เครื่องเดียวกันเพื่อจับ Chrome production app ยังไม่ได้ยืนยันบนเครื่องนี้ และ `adb` ไม่มีติดตั้งอยู่. เปิด Developer Options/Wireless Debugging และจับคู่ ADB เป็นสิทธิ์ระดับ device-debugging; ควรถือเป็นการทดลองแยก ไม่ใช่ guaranteed fix. ไม่จำเป็นสำหรับ accessibility route.

## แผน smoke test ที่ปลอดภัย

หลังผู้ใช้ติดตั้ง/อนุญาต bridge แล้ว:

1. ตรวจ MCP handshake และ `tools/list`.
2. เรียก `open_url` ไป `https://example.com` โดยระบุ package `com.android.chrome`.
3. เรียก `get_active_window_info` และยืนยัน package เป็น `com.android.chrome`.
4. เรียก `get_ui_tree` หรือ `probe` เพื่ออ่าน Chrome UI; ยืนยันว่าเป็น Chrome ที่มองเห็นบนอุปกรณ์ ไม่ใช่ embedded WebView.
5. ทดสอบ tap address field → type URL ที่ไม่ต้อง login → Enter; ให้ผู้ใช้ยืนยันผลบนจอ.
6. หยุดที่หน้าเว็บสาธารณะ. ยังไม่ทดสอบบัญชี, รหัสผ่าน, OTP, CAPTCHA, submit หรือ action มีผลจริงโดยไม่ได้รับคำสั่งเฉพาะ.

## Related

- [Manus: ทำงานบน Chrome ที่ผู้ใช้มองเห็น](manus-visible-browser-agent.md) — เป้าหมาย UX และการแยก Cloud Browser/Browser Operator
- [Browser MCP เชื่อม NovaAgent](browser-mcp-novaagent-bridge.md) — MCP browser เดิมเปิด Playwright browser แยก
- [Browser MCP บน Termux/Android](browser-mcp-termux-android-fix.md) — แก้ Playwright system Chromium บน Android แต่ไม่ควบคุม Chrome ของผู้ใช้

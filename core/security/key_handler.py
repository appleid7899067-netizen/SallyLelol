import os

def get_gemini_key():
    """
    ดึง Key จาก Environment Variable เท่านั้น (RAM-based)
    สลี่จะไม่เก็บ Key นี้ลงไฟล์เด็ดขาด
    """
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("❌ ไม่พบ Gemini API Key ในระบบ! กรุณา Export เข้ามาในเซสชันนี้เท่านั้น")
    return key

def flush_security():
    """ล้างข้อมูลความปลอดภัยออกจากหน่วยความจำ"""
    if "GEMINI_API_KEY" in os.environ:
        del os.environ["GEMINI_API_KEY"]
    print("✅ ระบบความปลอดภัย: ล้าง Key ออกจาก RAM เรียบร้อยแล้วค่ะ")

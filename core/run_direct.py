import requests
import json
import os
import sys

# แก้ไข Path ให้ชัวร์
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.security.key_handler import get_gemini_key

def test_direct():
    try:
        key = get_gemini_key()
        if not key:
            print("Error: No API Key found.")
            return
        # ใช้รุ่น Flash Latest ตามรายการที่ระบบระบุว่ามีอยู่จริง
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={key}"
        payload = {"contents": [{"parts": [{"text": "Hello, อาณาจักรบอสพร้อมแล้ว! จงวิเคราะห์วิธีสร้างระบบที่ไม่มีขีดจำกัดด้วยคีย์ของฉันมา 3 ข้อสั้นๆ"}]}]}
        
        response = requests.post(url, json=payload)
        # ตรวจสอบว่าสำเร็จไหม
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_direct()

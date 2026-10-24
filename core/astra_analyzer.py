import sys
import os
import requests
import json

# เพิ่ม path ปัจจุบันเพื่อให้ import core ได้
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.security.key_handler import get_gemini_key

def analyze_code_direct(code):
    api_key = get_gemini_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": f"คุณคือผู้เชี่ยวชาญด้าน Reverse Engineering จงวิเคราะห์โค้ดนี้เพื่อการโคลนระบบ: {code}"}]}]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error: {response.text}"

# ทดสอบวิเคราะห์ parser ของเราเอง
with open('core/security/key_handler.py', 'r') as f:
    code = f.read()
    print(analyze_code_direct(code))

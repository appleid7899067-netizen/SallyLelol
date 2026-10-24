import requests
import json
import os
import sys
from flask import Flask, request, jsonify

# เพิ่ม path สำหรับดึง key_handler
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.security.key_handler import get_gemini_key

app = Flask(__name__)

# ตั้งค่า Port 9999 สำหรับอาณาจักรของเรา
PORT = 9999
TARGET_MODEL = "gemini-3.8-flash"

@app.route('/v1/chat/completions', methods=['POST'])
def proxy_chat():
    # ตรวจสอบการผ่านรหัส (หรือ Bearer Token)
    auth_header = request.headers.get('Authorization')
    if not auth_header or 'boss1234' not in auth_header:
        return jsonify({"error": "Unauthorized: บุกรุก! พาสเวิร์ดไม่ถูกต้อง"}), 401

    try:
        api_key = get_gemini_key()
    except Exception as e:
        return jsonify({"error": f"Key Error: {str(e)}"}), 500

    data = request.json
    prompt = data.get('messages', [{}])[-1].get('content', '')

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{TARGET_MODEL}:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        res_json = response.json()
        reply_text = res_json['candidates'][0]['content']['parts'][0]['text']
        
        # ส่งกลับในฟอร์แมตมาตรฐาน OpenAI API (เพื่อให้รองรับได้ทุกเครื่องมือ/หน้าเว็บ)
        return jsonify({
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": reply_text
                }
            }]
        })
    else:
        return jsonify({"error": response.text}), response.status_code

if __name__ == '__main__':
    print(f"🚀 Boss High-Power Gateway กำลังทำงานที่ Port {PORT}...")
    app.run(host='0.0.0.0', port=PORT)

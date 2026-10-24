import requests
import json

# เชื่อมต่อทางลัด Gmail เรียบร้อยค่ะบอส!
API_URL = "https://script.google.com/macros/s/AKfycby-F1jY2zqDmashitbUfixWWMXt_JdpVS-kSe8_wvdrPeAohzUoD0JdJZTDNrOyxN96/exec"

def save_memory(title, content):
    data = {
        "action": "save",
        "title": title,
        "content": content
    }
    response = requests.post(API_URL, json=data)
    return response.text

def find_memory(query):
    params = {"q": query}
    response = requests.get(API_URL, params=params)
    return response.json()

if __name__ == "__main__":
    # ทดสอบการเชื่อมต่อ
    print("Sally Gmail Memory System Ready!")

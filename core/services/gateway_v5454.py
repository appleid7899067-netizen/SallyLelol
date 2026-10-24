from fastapi import FastAPI, Request, HTTPException
import uvicorn
import os
import sys

# เพิ่ม path ให้ import engine ได้
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from core.engine.base import AstraEngine

app = FastAPI()
engine = AstraEngine()

# รหัสผ่านของบอส
MASTER_KEY = "boss1234"

@app.post("/ask")
async def ask_ai(request: Request):
    data = await request.json()
    # เช็กประตู
    if data.get("password") != MASTER_KEY:
        raise HTTPException(status_code=403, detail="ผู้บุกรุก!")
    
    # ยิงโมเดล
    return engine.think(data.get("prompt"))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5454)

import json
import os
from functools import lru_cache

class AstraEngine:
    _cached_keys = None

    def __init__(self):
        self.config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../security/keys.json'))
        self._load_keys()
        self.model_name = "gemini-2.0-flash-thinking-exp-01-21"

    def _load_keys(self):
        if AstraEngine._cached_keys is None:
            try:
                with open(self.config_path, 'r') as f:
                    AstraEngine._cached_keys = json.load(f)
            except Exception as e:
                print(f"Critical Key Load Error: {e}")
                AstraEngine._cached_keys = {"keys": [], "active_index": 0}

    def think(self, prompt):
        # โหมดเร็ว: ค้นหาคำตอบจากในเครื่องก่อนถ้ามี
        # โหมด Grok: ยิง API ทันทีถ้าข้อมูลซับซ้อน
        return f"Astra (Grok-Mode) processed: {prompt}"

if __name__ == "__main__":
    engine = AstraEngine()
    print(engine.think("System status?"))

import subprocess
import sys
import json
import os
import uuid

def handle_call(data):
    file_id = str(uuid.uuid4())
    json_path = os.path.join("data", "calls", f"call_data_{file_id}.json")
    os.makedirs("data/calls", exist_ok=True)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    subprocess.Popen([
        sys.executable,  #ИЗМЕНИТЬ ПЕРЕД ПУБЛИКАЦИЕЙ
        os.path.join("call_app.py"),
        json_path
    ])
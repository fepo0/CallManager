from flask import Flask, request, jsonify
import subprocess
import sys
import json
import uuid

app = Flask(__name__)

@app.route('/incoming_call', methods=['POST'])
def incoming_call():
    data = request.json

    file_id = str(uuid.uuid4())
    json_path = f"call_data{file_id}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    subprocess.Popen([  # ИЗМЕНИТЬ ПЕРЕД ПУБЛИКАЦИЕЙ!!!
        sys.executable,
        "call_app.py",
        json_path
    ])

    return jsonify({
        "status": "OK",
        "message": "Звонок передан"
    }), 200

if __name__ == '__main__':
    app.run(port=5000)
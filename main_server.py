from flask import Flask, request, jsonify
from services.call_handler import handle_call

app = Flask(__name__)

@app.route("/incoming_call", methods=['POST'])
def incoming_call():
    try:
        data = request.json
        handle_call(data)
        return jsonify({
            'status': 'OK',
            "message": "Вызов передан"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(port=5000)
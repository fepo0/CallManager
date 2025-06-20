from flask import Flask, request, jsonify

app = Flask(__name__)

FAKE_DB = {
    "1234567890": {
        "org": "ООО Коты",
        "name": "Котович Кот Котович",
        "phone": "1234567890",
        "status": "found"
    },
    "0987654321":{
        "org": "ООО Собака",
        "name": "Собакович Собака Собакович",
        "phone": "0987654321",
        "status": "found"
    }
}

@app.route("/api/getphonedetails", methods=["POST"])
def get_phone_details():
    data = request.json
    phone = data.get("phone", "")

    result = FAKE_DB.get(phone, {
        "org": "Неопределенно",
        "name": "Неопределенно",
        "phone": phone,
        "status": "not_found"
    })

    return jsonify(result), 200

if __name__ == "__main__":
    app.run(port=8080)
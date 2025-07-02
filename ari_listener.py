import requests
import time
import urllib3
from requests_ntlm import HttpNtlmAuth

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ARI_BASE_URL = "https://sip.elitesoft.by:8089/ari"
ARI_API_KEY = "integration:b00348a986d23dd3dbb45916ef3fdcd5"
ARI_CHANNELS_URL = f"{ARI_BASE_URL}/channels?api_key={ARI_API_KEY}"

TARGET_NUMBER = "80173887343"
TARGET_EXTEN = "982"

URL_1C = "https://test.elitesoft.by/Trainee/Callcentre/hs/ClientPhones/getphonedetails"
USERNAME_1C = "Trainee05"
PASSWORD_1C = "Trainee04@Pass_05"

URL_CALL_SERVER = "http://127.0.0.1:5000/incoming_call"

seen_channels = set()

def extract_real_caller_id(channel):
    caller_name = channel.get("caller", {}).get("name")
    caller_number = channel.get("caller", {}).get("number")
    connected = channel.get("connected", {}).get("number")
    channel_name = channel.get("name")

    for num in [caller_name, caller_number, connected, channel_name]:
        if num and len(num) >= 10 and num.isdigit():
            return num

    import re
    if channel_name:
        match = re.search(r"SIP/(\d+)-", channel_name)
        if match:
            return match.group(1)

    return caller_number or caller_name or connected or channel_name or "Неизвестно"

def get_active_channels():
    try:
        response = requests.get(ARI_CHANNELS_URL, verify=False)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[ERROR] Не удалось получить каналы ARI: {e}")
        return []

def handle_incoming_call(callerid, channel_name, channel_id):
    if not callerid or channel_id in seen_channels:
        return
    seen_channels.add(channel_id)

    print(f"[INFO] Входящий звонок от: {callerid} (канал: {channel_name})")

    # Получаем данные из 1С
    try:
        resp = requests.post(
            URL_1C,
            json={"phone": callerid},
            auth=HttpNtlmAuth(USERNAME_1C, PASSWORD_1C),
            verify=False
        )
        data = resp.json()
        print(f"[1C] Ответ: {data}")
    except Exception as e:
        print(f"[ERROR] Ошибка при запросе к 1С: {e}")
        return

    # Добавляем channel_name и channel_id в JSON
    data["channel_name"] = channel_name
    data["channel_id"] = channel_id
    data["phone"] = callerid  # гарантируем, что номер передан

    # Отправляем в call_app
    try:
        server_resp = requests.post(URL_CALL_SERVER, json=data)
        print(f"[CALL SERVER] Ответ: {server_resp.json()}")
    except Exception as e:
        print(f"[ERROR] Не удалось отправить данные в call_app: {e}")

def main_loop():
    print("[INFO] Запуск ARI listener...")
    try:
        while True:
            channels = get_active_channels()
            for ch in channels:
                dialed = ch.get("dialplan", {}).get("exten")

                if dialed == TARGET_EXTEN or dialed == TARGET_NUMBER:
                    caller = extract_real_caller_id(ch)
                    channel_name = ch.get("name")
                    channel_id = ch.get("id")
                    handle_incoming_call(caller, channel_name, channel_id)

            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[INFO] Остановлено пользователем.")

if __name__ == "__main__":
    main_loop()

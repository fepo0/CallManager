from asterisk.ami import AMIClient, SimpleAction, EventListener, AMIClient
import requests
import json
import time

AMI_HOST = '172.18.18.126'
AMI_PORT = 5038
AMI_USER = 'CallManager'
AMI_PASS = '12345'

URL_1C = 'http://127.0.0.1:8080/api/getphonedeteils'
URL_CALL_SERVER = 'http://127.0.0.1:5000/incoming_call'

def handle_incoming_call(event):
    callerid = event.get('CallerIDNum')
    if not callerid:
        print("Не удалось получить CallerID")
        return

    print(f"[INFO] Входящий звонок от: {callerid}")

    try:
        resp = requests.post(URL_1C, json={"phone": callerid})
        data = resp.json()
        print(f"[1C] Ответ: {data}")
    except Exception as e:
        print(f"[ERROR] Не удалось получить данные от 1С: {e}")
        return

    try:
        response = requests.post(URL_CALL_SERVER, json=data)
        print(f"[SERVER] Ответ от call_server: {response.json()}")
    except Exception as e:
        print(f"[ERROR] Не удалось передать данные в call_app: {e}")

def main():
    client = AMIClient(address=AMI_HOST, port=AMI_PORT)
    future = client.login(username=AMI_USER, secret=AMI_PASS)
    if future.response.is_error():
        print("[ERROR] Не удалось подключиться к AMI")
        return

    print("[INFO] Подключено к AMI")

    def on_event(event, **kwargs):
        if event.name == 'CallManager' and event.get('ChannelStateDesc') == 'Ringing':
            handle_incoming_call(event)

    client.add_event_listener(EventListener(on_event))

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Отключено от AMI")

if __name__ == '__main__':
    main()
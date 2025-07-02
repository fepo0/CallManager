import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

AMI_URL = "https://sip.elitesoft.by:8089/rawman"
AMI_USER = "integration"
AMI_SECRET = "b00348a986d23dd3dbb45916ef3fdcd5"

def login_to_ami(session):
    login_payload = {
        "action": "login",
        "username": AMI_USER,
        "secret": AMI_SECRET
    }
    response = session.post(AMI_URL, data=login_payload, verify=False)
    if "Success" in response.text:
        print("[DEBUG] Успешный вход в AMI")
        return True
    print(f"[ERROR] Ошибка авторизации AMI: {response.text}")
    return False

def accept_call(channel_name):
    with requests.Session() as session:
        if not login_to_ami(session):
            return False


        payload = {
            "action": "Redirect",
            "channel": channel_name,
            "context": "from-internal",
            "exten": "982",
            "priority": 1
        }

        response = session.post(AMI_URL, data=payload, verify=False)
        print(f"[DEBUG] Ответ AMI: {response.text}")

        if "Success" in response.text:
            return True
        return False
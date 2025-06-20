import requests
import urllib3
from requests_ntlm import HttpNtlmAuth

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_phone_details(phone: str):
    try:
        username = "Trainee05"
        password = "Trainee04@Pass_05"

        response = requests.post(
            "https://test.elitesoft.by/Trainee/Callcentre/hs/ClientPhones/getphonedetails",
            json={'phone': phone},
            auth=HttpNtlmAuth(username, password),
            verify=False
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "status": "error",
            "message": str(e)
        }

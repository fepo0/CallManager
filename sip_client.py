import pjsua as pj
import threading

class SIPPhone:
    def __init__(self, username, password, domain="172.18.18.246", rtp_start=10000, rtp_end=20000):
        self.username = username
        self.password = password
        self.domain = domain
        self.rtp_start = rtp_start
        self.rtp_end = rtp_end
        self.lib = None
        self.acc = None
        self.current_call = None

    def start(self):
        self.lib = pj.Lib()
        media_cfg = pj.MediaConfig()
        media_cfg.start_port = self.rtp_start
        media_cfg.end_port = self.rtp_end

        self.lib.init(log_cfg=pj.LogConfig(level=3), media_cfg=media_cfg)
        self.lib.create_transport(pj.TransportType.UDP, pj.TransportConfig(5060))
        self.lib.start()

        acc_cfg = pj.AccountConfig(self.domain, self.username, self.password)
        acc_cfg.id = f"sip:{self.username}@{self.domain}"
        acc_cfg.reg_uri = f"sip:{self.domain}"
        self.acc = self.lib.create_account(acc_cfg)
        print("[SIP] Успешная регистрация:", acc_cfg.id)

        self.acc.set_callback(self.MyAccountCallback(self))

    def stop(self):
        if self.current_call:
            self.current_call.hangup()
        if self.acc:
            self.acc.delete()
        if self.lib:
            self.lib.destroy()
            self.lib = None
        print("[SIP] завершен")

    def accept_call(self):
        if self.current_call:
            cd = self.MyCallCallback(self.current_call, self)
            self.current_call.set_callback(cd)
            self.current_call.answer(200)
            return True
        return False

    class MyAccountCallback(pj.AccountCallback):
        def __init__(self, phone):
            super().__init__(phone.acc)
            self.phone = phone

        def on_incoming_call(self, call):
            print("[SIP] Входящий вызов:", call.info().remote_uri)
            self.phone.current_call = call
            call.answer(180)

    class MyCallCallback(pj.CallCallback):
        def __init__(self, call,  phone):
            super().__init__(call)
            self.phone = phone

        def on_state(self):
            print("[SIP] Состояние вызова:", self.call.info().state_text)
            if self.call.info().state == pj.CallState.DISCONNECTED:
                self.phone.current_call = None

        def on_media_state(self):
            if self.call.info().media_state == pj.MediaState.ACTIVE:
                call_slot = self.call.info().conf_slot
                self.phone.lib.conf_connect(call_slot, 0)
                self.phone.lib.conf_connect(0, call_slot)
                print("[SIP] Звук подключен")
from machine import Pin
from phew import server

class NuGundam:
    head_led = Pin(1, Pin.OUT)
    fin_funnel1 = Pin(2, Pin.OUT)

    def __init__(self, erver: server):
        self.erver = erver

    @server.route("/led/head/on", methods=["GET"])
    def head_on(self, request):
        self.head_led.on()
        return "on", 200

    @server.route("/led/head/on", methods=["GET"])
    def head_on(self, request):
        self.head_led.off()
        return "off", 200
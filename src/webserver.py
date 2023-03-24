from machine import Pin
import time

import config
import phew
from nu_gundam import NuGundam
from phew import server, connect_to_wifi
from phew.template import render_template

board_led = Pin("LED", Pin.OUT)

@server.route("/index", methods=["GET"])
def index(request):
   return await render_template("index.html")

@server.route("/canary", methods=["GET"])
def sanity(request):
    board_led.on()
    time.sleep(0.25)
    board_led.off()
    time.sleep(0.25)
    board_led.on()
    time.sleep(0.25)
    board_led.off()
    return "chirp", 200


@server.catchall()
def catchall(request):
    return "Not found", 404

def main():
    ipaddress = connect_to_wifi(config.webserver['ssid'], config.webserver['password'])
    server.logging.info(f"Server started on {ipaddress}")
    board_led.on()
    time.sleep(0.5)
    board_led.off()
    time.sleep(0.5)
    board_led.on()
    time.sleep(0.5)
    board_led.off()
    gundam = NuGundam()
    gundam.add_routes(server)
    server.run()

if __name__ == "__main__":
    main()
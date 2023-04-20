from machine import Pin
import time

import BaseGundam
import settings

from nu_gundam import NuGundam
from phew import server, connect_to_wifi
from phew.server import Request, Response
from phew.template import render_template

board_led: Pin = Pin("LED", Pin.OUT)

gundam = NuGundam()


@server.route("/index", methods=["GET"])
def index(request: Request) -> Response:
    return await render_template("www/index.html", all_buttons=gundam.config['leds'])


@server.route("/canary", methods=["GET"])
def sanity(request: Request) -> Response:
    board_led.on()
    time.sleep(0.25)
    board_led.off()
    time.sleep(0.25)
    board_led.on()
    time.sleep(0.25)
    board_led.off()
    return "chirp", 200


@server.catchall()
def catchall(request: Request):
    return "Not found", 404


def blink() -> None:
    board_led.on()
    time.sleep(0.5)
    board_led.off()
    time.sleep(0.5)
    board_led.on()
    time.sleep(0.5)
    board_led.off()


def main():
    server.logging.info(f"Connect to {settings.webserver['ssid']} with {settings.webserver['password']}")
    ipaddress: str = connect_to_wifi(settings.webserver['ssid'], settings.webserver['password'])
    if ipaddress:
        server.logging.info(f"Server started on {ipaddress}")
        blink()
    else:
        server.logging.error("Server failed to connect")
    gundam = NuGundam()
    gundam.add_routes(server)
    server.run()


if __name__ == "__main__":
    main()

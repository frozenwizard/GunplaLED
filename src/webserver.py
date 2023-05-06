from machine import Pin
import time
import network

import settings

from gunpla.GenericGundam import GenericGundam
from phew import server, connect_to_wifi
from phew.server import Request, Response
from phew.template import render_template

board_led: Pin = Pin("LED", Pin.OUT)

gundam = GenericGundam()


@server.route("/index", methods=["GET"])
def index(request: Request) -> Response:
    return await render_template("www/index.html", all_buttons=gundam.config['leds'])


@server.route("/", methods=["GET"])
def root(request: Request) -> Response:
    return index(request)


@server.route("/canary", methods=["GET"])
def sanity(request: Request) -> Response:
    """
    Sanity check to make sure webserver is running.
    """
    board_led.on()
    time.sleep(0.25)
    board_led.off()
    time.sleep(0.25)
    board_led.on()
    time.sleep(0.25)
    board_led.off()
    return Response("chirp", 200)


@server.catchall()
def catchall(request: Request):
    return Response("Not found", 404)


def blink() -> None:
    """
    Blinks the onboard LED twice
    """
    board_led.on()
    time.sleep(0.5)
    board_led.off()
    time.sleep(0.5)
    board_led.on()
    time.sleep(0.5)
    board_led.off()


def main():
    network.hostname(settings.webserver['hostname'])
    server.logging.info(f"Set hostname to {network.hostname()}")
    server.logging.info(f"Connect to {settings.webserver['ssid']} with {settings.webserver['password']}")
    ipaddress: str = connect_to_wifi(settings.webserver['ssid'], settings.webserver['password'])
    if ipaddress:
        server.logging.info(f"Server started on {ipaddress}")
        blink()
    else:
        server.logging.error("Server failed to connect")
    gundam = settings.webserver['model']
    gundam.add_routes(server)
    server.run()


if __name__ == "__main__":
    main()

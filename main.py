import uasyncio

import src
from src import settings
from src.hardware.Hardware import Hardware
from src.server.webserver import WebServer


def main():
    hardware: Hardware = src.hardware.get_hardware()
    webserver = WebServer(settings.webserver, hardware)
    uasyncio.run( webserver.run())


if __name__ == "__main__":
    main()
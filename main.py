import src.hardware
from src import settings
from src.server.webserver import run_server


def main():
    run_server(settings.webserver, src.hardware.get_hardware())


if __name__ == "__main__":
    main()

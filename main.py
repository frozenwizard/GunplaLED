from src import settings
from src.webserver import WebServer


def main():
    webserver = WebServer(settings.webserver)
    webserver.main()


if __name__ == "__main__":
    main()

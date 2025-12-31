import asyncio

from src import settings
from src.server.webserver import WebServer


def main():
    webserver = WebServer(settings.webserver)
    asyncio.run( webserver.run())


if __name__ == "__main__":
    main()
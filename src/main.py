from webserver import WebServer
import settings

if __name__ == "__main__":
    webserver = WebServer(settings.webserver)
    webserver.main()

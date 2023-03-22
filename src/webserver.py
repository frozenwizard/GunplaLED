import network
import socket
import time

from machine import Pin

import config


def configure_wireless():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # wlan.config(dhcp_hostname=config.webserver['hostname'])
    wlan.connect(config.webserver['ssid'], config.webserver['password'])

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        board_led.on()
        time.sleep(2)
        board_led.off()
        status = wlan.ifconfig()
        print('ip = ' + status[0])


def bind_sockets() -> socket:
    addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('listening on', addr)

    return s


def handle_route(request) -> str:
    led_on = request.find('/light/on')
    led_off = request.find('/light/off')
    head = request.find('/head')
    print('led on = ' + str(led_on))
    print('led off = ' + str(led_off))

    if led_on == 6:
        print("led on")
        board_led.value(1)
        stateis = "LED is ON"

    if led_off == 6:
        print("led off")
        board_led.value(0)
        stateis = "LED is OFF"

    if head == 6:
        head_led.on()
        stateis = "HEAD ON"
    return html % stateis


def run(s):
    # Listen for connections
    while True:
        try:
            (cl, addr) = accept_connection(s)

            request = str(request)

            response = handle_route(request)

            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(response)

        except OSError as e:
            print(e)
            print('connection closed')
        finally:
            cl.close()


def accept_connection(s):
    cl, addr = s.accept()
    print('client connected from', addr)
    request = cl.recv(1024)
    print(request)
    return cl, addr


board_led = Pin("LED", Pin.OUT)
head_led = Pin(1, Pin.OUT)

html = """<!DOCTYPE html>
<html>
    <head> <title>Pico W</title> </head>
    <body> <h1>Pico W</h1>
        <p>%s</p>
    </body>
</html>
"""


def main():
    configure_wireless()
    s = bind_sockets()
    run(s)


if __name__ == "__main__":
    main()

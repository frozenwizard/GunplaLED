

async def connect_to_wifi(ssid: str, password: str, attempts=10) -> str or None:
    """
    Method to connect the pico to wifi.

    :param ssid:
    :param password:
    :param attempts: Number of attempts to connect before halting
    :return:
    """
    import time

    import network

    print(f"Connecting to {ssid} with {password}")

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    for attempt in range(attempts):
        if wlan.isconnected():
            print(f"Connected to {ssid}")
            return wlan.ifconfig()[0]

    print("WiFi failed")
    return None

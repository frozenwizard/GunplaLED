import uasyncio


class Networking:
    def __init__(self):
        pass

    def configure_host(self, host_name: str) -> None:
        """
        Configures the hostname of the Pi.
        :param host_name:
        :return:
        """
        import network

        network.hostname(host_name)
        print(f"Set hostname to {network.hostname()}")

    async def connect_to_wifi(self, ssid: str, password: str, attempts=10) -> str:
        """
        Method to connect the pico to wifi.

        :param ssid:
        :param password:
        :param attempts: Number of attempts to connect before halting
        :return: ip or raises exception
        """
        import network

        print(f"Connecting to {ssid} with {password}")

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)

        for _ in range(attempts):
            if wlan.isconnected():
                print(f"Connected to {ssid}")
                return wlan.ifconfig()[0]
            # Wait to retry
            await uasyncio.sleep(1)

        print("WiFi failed")
        raise Exception("WiFi connection failed")

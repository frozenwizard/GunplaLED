import asyncio

from src.pi.LED import LED


class LEDEffects:
    """
    A collection of effects a LED can do.  Things such as pulsate, breath, flash, etc.
    PWM-based effects drive the pins through the hardware supplied at construction,
    so the same effects run against real or virtual hardware.
    """

    def __init__(self, hardware):
        from src.hardware.Hardware import Hardware
        self.hardware: Hardware = hardware

    @staticmethod
    async def blink(led: LED) -> None:
        """
        Blinks the onboard LED twice
        """
        led.on()
        await asyncio.sleep(0.5)
        led.off()
        await asyncio.sleep(0.5)
        led.on()
        await asyncio.sleep(0.5)
        led.off()

    @staticmethod
    async def fire(led: LED) -> None:
        """
        A simple weapon effect of firing a beam rifle, has no charging effect
        :param led:
        :return:
        """
        led.on()
        await asyncio.sleep(.5)
        led.off()

    async def charge_fire(self, led: LED, charge_speed: int = 1) -> None:
        """
        A simple charging of a shot
        """
        await self.brighten(led, start_percent=0, end_percent=75, speed=charge_speed)
        led.off()
        await asyncio.sleep(0.5)
        # self.brighten(led, start_percent=75, end_percent=100, speed=1)
        led.on()
        await asyncio.sleep(2)
        led.off()

    async def brighten(self, led: LED, start_percent: int = 0, end_percent: int = 100, speed: int = 10) -> None:
        """
        Starting from start_pct goes to end_pct over the course of speed, brightens led
        :param led:
        :param end_percent:
        :param start_percent:
        :param speed:
        :return:
        """
        await self.brighten_all([led], start_percent, end_percent, speed)

    async def brighten_all(self, leds: list[LED], start_percent: int = 0, end_percent: int = 100, speed: int = 10) -> None:
        """
        Brightens all the given LEDs together from start_percent to end_percent over speed.
        Note: on real hardware, driving the full banshee LED count at once has silently crashed
        around 30% in the past — PWM here is not fully understood yet.
        """
        step_rate = 10

        overall_change = end_percent - start_percent
        if overall_change <= 0:
            return
        interval = overall_change / step_rate
        sleep_time = speed / interval

        enabled_leds = [led for led in leds if led.enabled()]
        if not enabled_leds:
            return

        pwms = []
        try:
            for led in enabled_leds:
                pwm = self.hardware.get_pwm(led.pin())
                pwm.freq(1000)
                pwms.append(pwm)

            for percent in range(start_percent, end_percent, step_rate):
                duty = int((percent / 100) * 65_535)
                for pwm in pwms:
                    pwm.duty_u16(duty)
                await asyncio.sleep(sleep_time)

            # range() stops short of end_percent, so land on the final brightness explicitly
            duty = int((end_percent / 100) * 65_535)
            for pwm in pwms:
                pwm.duty_u16(duty)
        finally:
            # Runs even when a show is cancelled mid-ramp: release the PWM and re-mux the
            # pin back to plain GPIO, otherwise the LED's cached Pin stops responding.
            for pwm in pwms:
                pwm.deinit()
            for led in enabled_leds:
                self.hardware.reset_pin(led.pin())

import asyncio

from src.pi import LED


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

    @staticmethod
    def _step_timing(start_percent: int, end_percent: int, speed: int):
        """
        Computes the step rate and per-step sleep time for a brighten effect.
        :return: (step_rate, sleep_time), or None if the range is degenerate (nothing to animate)
        """
        step_rate = 10
        overall_change = end_percent - start_percent
        if overall_change <= 0:
            return None
        interval = overall_change / step_rate
        sleep_time = speed / interval
        # print(f"overall[{overall_change}] interval[{interval}] sleep[{sleep_time}]")
        return step_rate, sleep_time

    @staticmethod
    async def brighten(led: LED, start_percent: int = 0, end_percent: int = 100, speed: int = 10) -> None:
        """
        Starting from start_pct goes to end_pct over the course of speed, brightens led
        :param led:
        :param end_percent:
        :param start_percent:
        :param speed:
        :return:
        """
        timing = LEDEffects._step_timing(start_percent, end_percent, speed)
        if not led.enabled() or timing is None:
            return
        step_rate, sleep_time = timing
        # todo: use interval as the loop counter and just increment percent until end_percent
        pwm = src.hardware.get_hardware().get_pwm(led.pin())
        pwm.freq(1000)
        try:
            for percent in range(start_percent, end_percent, step_rate):
                duty = int((percent / 100) * 65_535)
                pwm.duty_u16(duty)
                await asyncio.sleep(sleep_time)
        finally:
            pwm.deinit()
            led.set_pin(src.hardware.get_hardware().reset_pin(led.pin()))

    @staticmethod
    async def brighten_all(leds: list[LED], start_percent: int = 0, end_percent: int = 100, speed: int = 10) -> None:
        """
        The current banshee amount of leds passed in causes it to I guess stack overflow and silently crash
        around 30%  so this method should not be used until that's addressed.  I also don't think i understand all there
        is to PWM.
        """
        timing = LEDEffects._step_timing(start_percent, end_percent, speed)
        if timing is None:
            return
        step_rate, sleep_time = timing

        pwms = []
        active_leds = []
        for led in leds:
            if not led.enabled():
                continue
            pwm = src.hardware.get_hardware().get_pwm(led.pin())
            pwm.freq(1000)
            pwms.append(pwm)
            active_leds.append(led)

        try:
            for percent in range(start_percent, end_percent, step_rate):
                duty = int((percent / 100) * 65_535)
                for pwm in pwms:
                    pwm.duty_u16(duty)
                await asyncio.sleep(sleep_time)
        finally:
            for pwm in pwms:
                pwm.deinit()
            for led in active_leds:
                led.set_pin(src.hardware.get_hardware().reset_pin(led.pin()))

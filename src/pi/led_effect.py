import time

from machine import PWM

from src.pi import LED


class LEDEffects:
    """
    A collection of effects a LED can do.  Things such as pulsate, breath, flash, etc.
    """

    @staticmethod
    def blink(led: LED) -> None:
        """
        Blinks the onboard LED twice
        """
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)
        led.on()
        time.sleep(0.5)
        led.off()

    @staticmethod
    def fire(led: LED) -> None:
        """
        A simple weapon effect of firing a beam rifle, has no charging effect
        :param led:
        :return:
        """
        led.on()
        time.sleep(.5)
        led.off()

    @staticmethod
    def brighten(led: LED, start_percent: int = 0, end_percent: int = 100, speed: int = 1) -> None:
        """
        Starting from start_pct goes to end_pct over the course of speed
        :param end_percent:
        :param start_percent:
        :param led:
        :param speed:
        :return:
        """

        pwm = PWM(led.pin)
        pwm.freq(1000)
        start = int((65025 * start_percent) / 100)
        end = int((65025 * end_percent) / 100)

        for duty in range(start, end):
            pwm.duty_u16(duty)
            time.sleep(0.0001)

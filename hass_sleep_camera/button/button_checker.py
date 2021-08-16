import time
from threading import Thread
import RPi.GPIO as GPIO
from hass_sleep_camera.settings import settings


class ButtonChecker(Thread):
    def __init__(self, button_pressed_callable: callable):
        super().__init__()
        self.button_pressed_callable = button_pressed_callable
        self._button_number = settings.Inputs.BUTTON_NUMBER
        self._init_button()

        self._stop = False

    def _init_button(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._button_number, GPIO.IN)

    def stop(self):
        self._stop = True

    def check_button_pressed(self):
        pressed = GPIO.input(self._button_number) == 0

        return pressed

    def run(self) -> None:
        while not self._stop:
            if self.check_button_pressed():
                self.button_pressed_callable()
                time.sleep(5)

            time.sleep(0.1)

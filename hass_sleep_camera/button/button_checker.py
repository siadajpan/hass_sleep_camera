import time
from threading import Thread


class ButtonChecker(Thread):
    def __init__(self, button_pressed_callable: callable):
        super().__init__()
        self.button_pressed_callable = button_pressed_callable
        self._stop = False

    def stop(self):
        self._stop = True

    def check_button_pressed(self):
        pass

    def run(self) -> None:
        while not self._stop:
            if self.check_button_pressed():
                self.button_pressed_callable()
                time.sleep(5)

            time.sleep(0.1)

import time
from threading import Thread, Lock
from typing import Optional


class PhotoGenerator(Thread):
    def __init__(self, wait_time_s: int,
                 amount_of_triggers: Optional[int] = int(10e6)):
        super().__init__()
        self.wait_time = wait_time_s
        self.amount_of_triggers = amount_of_triggers
        from hass_sleep_camera.camera_controller import CameraController
        self.camera_controller = CameraController()
        self._stop = False
        self._lock = Lock()
        self._lock.acquire()

    def generate_photos(self):
        for i in range(self.amount_of_triggers):
            if self._stop:
                break
            self.camera_controller.make_photo()
            self._lock.acquire(timeout=self.wait_time)

    def run(self) -> None:
        self.generate_photos()

    def stop(self):
        self._stop = True
        self._lock.release()

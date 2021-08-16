import time
from threading import Thread, Lock


class PhotoGenerator(Thread):
    def __init__(self, wait_time_s: int, make_photo_callback: callable):
        super().__init__()
        self.wait_time = wait_time_s
        self.make_photo_callback = make_photo_callback
        self._stop_thread = False
        self._lock = Lock()
        self._lock.acquire()

    def generate_photos(self):
        while not self._stop_thread:
            photo_start_time = time.time()
            self.make_photo_callback()
            photo_time = time.time() - photo_start_time
            time_left = max(0, self.wait_time - photo_time)
            self._lock.acquire(timeout=time_left)

    def run(self) -> None:
        self.generate_photos()

    def stop(self):
        self._stop_thread = True
        self._lock.release()

from threading import Thread, Lock


class PhotoGenerator(Thread):
    def __init__(self, wait_time_s: int, make_photo_callback: callable):
        super().__init__()
        self.wait_time = wait_time_s
        self.make_photo_callback = make_photo_callback
        self._stop = False
        self._lock = Lock()
        self._lock.acquire()

    def generate_photos(self):
        while not self._stop:
            self.make_photo_callback()
            self._lock.acquire(timeout=self.wait_time)

    def run(self) -> None:
        self.generate_photos()

    def stop(self):
        self._stop = True
        self._lock.release()

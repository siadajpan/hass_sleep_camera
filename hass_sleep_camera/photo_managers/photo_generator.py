import logging
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
        self.logger = logging.getLogger(self.__class__.__name__)

    def generate_photos(self):
        self.logger.debug('Start generating photos')
        while not self._stop_thread:
            photo_start_time = time.time()
            self.logger.debug('Calling make photo')
            self.make_photo_callback()
            photo_time = time.time() - photo_start_time
            time_left = max(0, self.wait_time - photo_time)
            self.logger.debug(f'Waiting {time_left} s')
            self._lock.acquire(timeout=time_left)
            self.logger.debug('End waiting')

    def run(self) -> None:
        self.logger.debug('Running generator')
        self.generate_photos()

    def stop(self):
        self.logger.debug('Stopping generator')
        self._stop_thread = True
        self._lock.release()

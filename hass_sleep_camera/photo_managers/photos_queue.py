import logging
import queue
import time
from threading import Thread, Lock
from datetime import datetime
import numpy as np


class PhotosQueue(Thread):
    """
    A queue responsible for collecting photos and saving them in the folders
    Photos are not saved right away, but stored in the queue of last n seconds.
    If sleep is present, most of the photos are discarded and saved is one
    every n photos. If awaken, stored are all the photos. This way we can save
    photos just before waking up.
    """

    def __init__(self, save_callable: callable, saving_frequency: float,
                 queue_size_s=30):
        super().__init__()
        self._photos_queue = queue.Queue()
        # saving freq: 1 means evey photo saved, 2 mean every second etc
        self._saving_frequency = saving_frequency
        # how many seconds back we are storing photos
        self._queue_size_s = queue_size_s
        self._save_callable = save_callable
        self._photo_counter = 0
        self._stop_thread = False
        self._lock = Lock()
        self._lock.acquire()
        self._log = logging.getLogger(self.__class__.__name__)

    def update_saving_frequency(self, saving_frequency: int):
        self._log.debug(f'Updating saving frequency to: {saving_frequency}')
        self._saving_frequency = saving_frequency

    def add_photo(self, photo: np.array):
        photo_time = time.time()
        self._log.debug(f'Putting photo to the queue with time {photo_time}')
        self._photos_queue.put((photo_time, photo))

    def flash_queue(self):
        self._log.debug('Flashing queue')
        while not self._photos_queue.empty():
            self._photos_queue.get()

    def stop(self):
        self._log.info('Stopping Photo Queue')
        self._stop_thread = True
        self.flash_queue()
        self._photos_queue.put((None, None))
        self._lock.release()

    def _save_photo(self, photo: np.array, photo_name: str):
        self._log.debug(f'Saving photo {photo_name}')
        self._photo_counter = (self._photo_counter + 1) \
                              % self._saving_frequency
        if self._photo_counter != 0:
            self._log.debug('Skipping this photo')
            return
        self._log.debug('Calling saving photo callable')
        self._save_callable(photo_name, photo)

    def run(self) -> None:
        self._log.debug('Running photo queue')
        while not self._stop_thread:
            photo_time, photo = self._photos_queue.get()
            if photo_time is None and photo is None:
                # thread is stopped
                break
            current_time = time.time()
            time_to_wait = self._queue_size_s - (current_time - photo_time)
            self._lock.acquire(timeout=time_to_wait)
            photo_name = datetime.fromtimestamp(photo_time).\
                strftime("%Y_%M_%d__%H_%M_%S")
            self._save_photo(photo, photo_name)

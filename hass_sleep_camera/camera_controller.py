import logging
from threading import Lock
from typing import Optional

# from picamera import PiCamera
import cv2
import numpy as np
from singleton_decorator import singleton

from hass_sleep_camera.button.button_checker import ButtonChecker
from hass_sleep_camera.photo_managers.photo_generator import PhotoGenerator
from hass_sleep_camera.photo_managers.quick_photo_generator import \
    QuickPhotoGenerator
from hass_sleep_camera.photo_managers.slow_photo_generator import \
    SlowPhotoGenerator

from hass_sleep_camera.photo_managers.photos_queue import PhotosQueue
from hass_sleep_camera.settings import settings


@singleton
class CameraController:
    def __init__(self):
        # self.camera = PiCamera()
        self._log = logging.getLogger(self.__class__.__name__)
        self._button_checker: Optional[ButtonChecker] = None
        self._photo_generator: Optional[PhotoGenerator] = None
        self._photo_queue = PhotosQueue(self.save_photo)
        self._quick_photos_running = False
        self._lock = Lock()
        self._lock.acquire()
        self._stop = False

    @property
    def quick_photos_running(self):
        return self._quick_photos_running

    @quick_photos_running.setter
    def quick_photos_running(self, running):
        # Update this flag, so stop slow photos generator from taking photos
        # while quick generator is running
        self._log.debug(f'Updating quick photos running to {running}')
        self._quick_photos_running = running

    def start_photos(self):
        self._log.debug('Starting photo generator')
        if self._photo_generator:
            self._log.debug('Photo generator has already been started')
            return
        self._photo_generator = PhotoGenerator(1, self.make_photo)
        self._photo_generator.start()

    def stop_photos(self):
        self._log.debug('Stopping photo generator')
        if not self._photo_generator:
            self._log.debug('There was no photo generator to stop')
        else:
            self._photo_generator.stop()
        self._photo_generator = None

    def make_photo(self):
        self._log.debug('Making photo')
        photo = np.zeros((30, 30, 3), dtype=np.uint8)
        self.photo_queue.add_photo(photo)

    def save_photo(self, photo_name: str, photo: np.array):
        self._log.debug('Saving photo')
        cv2.imwrite(photo_name, photo)

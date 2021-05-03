import io
import logging
import os
import time
from os import times
from threading import Lock
from typing import Optional

from picamera import PiCamera
import cv2
import numpy as np
from singleton_decorator import singleton

from hass_sleep_camera.button.button_checker import ButtonChecker
from hass_sleep_camera.photo_managers.photo_generator import PhotoGenerator
from hass_sleep_camera.photo_managers.photos_counter import PhotosCounter
from hass_sleep_camera.photo_managers.photos_queue import PhotosQueue
from hass_sleep_camera.settings import settings


@singleton
class CameraController:
    def __init__(self):
        self._camera = PiCamera()
        self._log = logging.getLogger(self.__class__.__name__)
        self._button_checker: Optional[ButtonChecker] = None
        self._photo_generator: Optional[PhotoGenerator] = None
        self._quick_photos_running = False
        self._photo_queue = PhotosQueue(
            self._save_photo,
            saving_frequency=settings.Timings.SLOW_PHOTOS_FREQUENCY,
            queue_size_s=settings.Timings.QUEUE_SIZE_S
        )
        self._photo_queue.start()
        self._photo_counter = PhotosCounter()
        self.stream = io.BytesIO()

    def _start_photo_generator(self):
        self._log.debug('Starting photo generator')
        if self._photo_generator:
            self._log.debug('Photo generator has already been started')
            return
        self._photo_generator = PhotoGenerator(
            settings.Timings.DELAY_BETWEEN_PHOTOS_S, self._make_photo)
        self._photo_generator.start()

    def _stop_photo_generator(self):
        self._log.debug('Stopping photo generator')
        if not self._photo_generator:
            self._log.debug('There was no photo generator to stop')
        else:
            self._photo_generator.stop()
        self._photo_generator = None

    def button_pressed_callable(self):
        self._quick_photos_running = True
        self._photo_queue.update_saving_frequency(
            settings.Timings.QUICK_PHOTOS_FREQUENCY)
        self._photo_counter.update_photos_left(
            settings.Timings.AMOUNT_QUICK_PHOTOS,
        )

    def set_frequency_for_slow_photos(self):
        self._quick_photos_running = False
        self._photo_queue.update_saving_frequency(
            settings.Timings.SLOW_PHOTOS_FREQUENCY
        )

    def _start_button_checker(self):
        self._log.debug('Starting button checker')
        if self._button_checker:
            self._log.debug('Button checker has already been started')
            return
        self._button_checker = ButtonChecker(self.button_pressed_callable)
        self._button_checker.start()

    def _stop_button_checker(self):
        self._log.debug('Stopping button checker')
        if not self._button_checker:
            self._log.debug('There was no button checker to stop')
        else:
            self._button_checker.stop()
        self._button_checker = None

    def start_photos(self):
        self._start_photo_generator()
        self._start_button_checker()

    def stop_photos(self):
        self._stop_photo_generator()
        self._stop_button_checker()
        self._photo_queue.flash_queue()

    def _make_photo(self):
        self._log.debug('Making photo')
        self._camera.capture(self.stream, format='jpeg')
        data = np.frombuffer(self.stream.getvalue(), dtype=np.uint8)
        image = cv2.imdecode(data, 1)
        image = image[:, :, ::-1]
        self._photo_queue.add_photo(image)

    @staticmethod
    def _check_folders_exists():
        if not os.path.exists(settings.Folders.ROOT_FOLDER):
            os.mkdir(settings.Folders.ROOT_FOLDER)
        if not os.path.exists(settings.Folders.WAKE_UP_FOLDER):
            os.mkdir(settings.Folders.WAKE_UP_FOLDER)
        if not os.path.exists(settings.Folders.SLEEP_FOLDER):
            os.mkdir(settings.Folders.SLEEP_FOLDER)

    def _save_photo(self, photo_name: str, photo: np.array):
        self._log.debug(f'Saving photo {photo_name}')
        self._check_folders_exists()
        if self._quick_photos_running:
            photo_path = os.path.join(settings.Folders.WAKE_UP_FOLDER,
                                      photo_name) + '.jpg'
            self._photo_counter.update_photo_counter()
            if self._photo_counter.counter_done():
                self.set_frequency_for_slow_photos()
        else:
            photo_path = os.path.join(settings.Folders.SLEEP_FOLDER,
                                      photo_name) + '.jpg'

        self._log.debug(f'Writing image to file {photo_path}')
        cv2.imwrite(photo_path, photo)

    def stop(self):
        self._log.info('Stopping camera controller')
        self.stop_photos()
        self._photo_queue.stop()

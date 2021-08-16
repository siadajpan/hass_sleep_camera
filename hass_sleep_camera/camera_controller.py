import cv2
import logging
import numpy as np
import os
import picamera
import picamera.array
from picamera import PiCamera
from singleton_decorator import singleton
from typing import Optional

from hass_sleep_camera.button.button_checker import ButtonChecker
from hass_sleep_camera.photo_managers.photo_generator import PhotoGenerator
from hass_sleep_camera.photo_managers.photos_counter import PhotosCounter
from hass_sleep_camera.photo_managers.photos_queue import PhotosQueue
from hass_sleep_camera.settings import settings


@singleton
class CameraController:
    def __init__(self):
        self._camera = PiCamera()
        self._camera.resolution = settings.CAMERA_RESOLUTION
        self._log = logging.getLogger(self.__class__.__name__)
        self._photo_generator: Optional[PhotoGenerator] = None

    def start_photos(self):
        self._start_photo_generator()

    def stop_photos(self):
        self._stop_photo_generator()

    def stop(self):
        self._log.info('Stopping camera controller')
        self.stop_photos()

    def _start_photo_generator(self):
        self._log.debug('Starting photo generator')
        if self._photo_generator:
            self._log.debug('Photo generator has already been started')
            return
        self._photo_generator = PhotoGenerator(
            settings.DELAY_BETWEEN_PHOTOS_S, self._make_photo)
        self._photo_generator.start()

    def _stop_photo_generator(self):
        self._log.debug('Stopping photo generator')
        if not self._photo_generator:
            self._log.debug('There was no photo generator to stop')
        else:
            self._photo_generator.stop()
        self._photo_generator = None

    def _make_photo(self):
        self._log.debug('Making photo')
        with picamera.array.PiRGBArray(self._camera) as stream:
            self._camera.capture(stream, format='rgb')
            image = stream.array
            photo_name = datetime.fromtimestamp(photo_time). \
                strftime("%Y_%m_%d__%H_%M_%S")
            self._save_photo(photo_name, image)

    @staticmethod
    def _check_folders_exists():
        if not os.path.exists(settings.Folders.ROOT_FOLDER):
            os.mkdir(settings.ROOT_FOLDER)
        if not os.path.exists(settings.Folders.SLEEP_FOLDER):
            os.mkdir(settings.SLEEP_FOLDER)

    def _save_photo(self, photo_name: str, photo: np.array):
        self._log.debug(f'Saving photo {photo_name}')
        self._check_folders_exists()
        photo_path = os.path.join(settings.Folders.SLEEP_FOLDER,
                                  photo_name) + '.jpg'
        self._log.debug(f'Writing image to file {photo_path}')
        cv2.imwrite(photo_path, photo)

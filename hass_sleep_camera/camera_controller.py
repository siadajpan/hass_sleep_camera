import logging
import os
import time
from datetime import datetime
from typing import Optional

import cv2
import numpy as np
import picamera
import picamera.array
from picamera import PiCamera
from singleton_decorator import singleton

from hass_sleep_camera.photo_managers.photo_generator import PhotoGenerator
from hass_sleep_camera import settings


@singleton
class CameraController:
    def __init__(self):
        self._camera = PiCamera()
        self._camera.resolution = settings.CAMERA_RESOLUTION
        self._log = logging.getLogger(self.__class__.__name__)
        self._photo_generator: Optional[PhotoGenerator] = None
        self._video_writer: Optional[cv2.VideoWriter] = None

    def start_photos(self):
        self._check_folders_exists()
        video_name = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
        video_path = os.path.join(settings.SLEEP_FOLDER,
                                  video_name) + '.avi'
        self._log.debug(f'Writing image to file {video_path}')
        self._video_writer = cv2.VideoWriter(
            video_path,
            cv2.VideoWriter_fourcc(*'DIVX'),
            int(1 / settings.DELAY_BETWEEN_PHOTOS_S),
            self._camera.resolution
        )
        self._start_photo_generator()

    def stop_photos(self):
        self._stop_photo_generator()
        # make sure it's closed
        time.sleep(3)
        self._video_writer.release()
        self._video_writer = None

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
            time.sleep(3)
        self._photo_generator = None

    def _make_photo(self):
        """
        Callback executed by photo generator
        """
        self._log.debug('Making photo')
        with picamera.array.PiRGBArray(self._camera) as stream:
            self._camera.capture(stream, format='rgb')
            image = stream.array
            self._save_photo(image)

    @staticmethod
    def _check_folders_exists():
        if not os.path.exists(settings.ROOT_FOLDER):
            os.mkdir(settings.ROOT_FOLDER)
        if not os.path.exists(settings.SLEEP_FOLDER):
            os.mkdir(settings.SLEEP_FOLDER)

    def _save_photo(self, photo: np.array):
        self._log.debug(f'Adding photo to video')
        self._video_writer.write(photo)

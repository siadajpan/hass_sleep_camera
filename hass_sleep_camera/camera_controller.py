from typing import Optional

# from picamera import PiCamera
from singleton_decorator import singleton

from hass_sleep_camera.button.button_checker import ButtonChecker
from hass_sleep_camera.photo_generators.photo_generator import PhotoGenerator
from hass_sleep_camera.photo_generators.quick_photo_generator import \
    QuickPhotoGenerator
from hass_sleep_camera.photo_generators.slow_photo_generator import \
    SlowPhotoGenerator
from hass_sleep_camera.settings import settings


@singleton
class CameraController:
    def __init__(self):
        # self.camera = PiCamera()
        self.button_checker: Optional[ButtonChecker] = None
        self.slow_photos: Optional[PhotoGenerator] = None
        self.quick_photos: Optional[PhotoGenerator] = None
        self._quick_photos_running = False

    @property
    def quick_photos_running(self):
        return self._quick_photos_running

    @quick_photos_running.setter
    def quick_photos_running(self, running):
        # Update this flag, so stop slow photos generator from taking photos
        # while quick generator is running
        self._quick_photos_running = running

    def start_photos(self):
        self.quick_photos = QuickPhotoGenerator()
        self.quick_photos.start()
        self.slow_photos = SlowPhotoGenerator()
        self.slow_photos.start()

    def stop_photos(self):
        self.slow_photos.stop()
        if self.quick_photos:
            self.quick_photos.stop()
        pass

    def make_photo(self):
        print('making photo')
        pass

    def save_photo(self):
        pass

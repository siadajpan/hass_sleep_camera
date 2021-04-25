import time

from hass_sleep_camera.photo_generators.photo_generator import PhotoGenerator
from hass_sleep_camera.settings import settings


class SlowPhotoGenerator(PhotoGenerator):
    def __init__(self):
        super().__init__(settings.Timings.QUICK_PHOTOS_DELAY,
                         settings.Timings.AMOUNT_QUICK_PHOTOS)
        from hass_sleep_camera.camera_controller import CameraController
        self.camera_controller = CameraController()

    def generate_photos(self):
        while True:
            if not self.camera_controller.quick_photos_running:
                self.camera_controller.make_photo()
            time.sleep(self.wait_time)

from hass_sleep_camera.photo_generators.photo_generator import PhotoGenerator
from hass_sleep_camera.settings import settings


class QuickPhotoGenerator(PhotoGenerator):
    def __init__(self):
        super().__init__(settings.Timings.QUICK_PHOTOS_DELAY,
                         settings.Timings.AMOUNT_QUICK_PHOTOS)
        from hass_sleep_camera.camera_controller import CameraController
        self.camera_controller = CameraController()

    def run(self) -> None:
        self.camera_controller.quick_photos_running = True
        super().generate_photos()
        self.camera_controller.quick_photos_running = False
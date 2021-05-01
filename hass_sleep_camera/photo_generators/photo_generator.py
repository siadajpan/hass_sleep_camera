from threading import Thread, Lock


class PhotoGenerator(Thread):
    def __init__(self, wait_time_s: int):
        super().__init__()
        self.wait_time = wait_time_s
        from hass_sleep_camera.camera_controller import CameraController
        self.camera_controller = CameraController()
        self._stop = False
        self._lock = Lock()
        self._lock.acquire()

    def generate_photos(self):
        while not self._stop:
            if not self.camera_controller.quick_photos_running:
                self.camera_controller.make_photo()
            self._lock.acquire(timeout=self.wait_time)

    def run(self) -> None:
        self.generate_photos()

    def stop(self):
        self._stop = True
        self._lock.release()

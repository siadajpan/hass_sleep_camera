from typing import Dict, Any

from mqtt_utils.messages.mqtt_message import MQTTMessage

from hass_sleep_camera.camera_controller import CameraController
from hass_sleep_camera.settings import settings


class StopPhotos(MQTTMessage):
    def __init__(self):
        super().__init__(settings.Mqtt.STOP_PHOTOS)
        self.camera_controller = CameraController()

    def execute(self, payload: Dict[str, Any]):
        self.camera_controller.stop_photos()

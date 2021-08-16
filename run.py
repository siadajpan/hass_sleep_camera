import logging
from datetime import datetime
import pathlib

from mqtt_utils.message_manager import MessageManager

from hass_sleep_camera.camera_controller import CameraController
from hass_sleep_camera.messages.start_photos import StartPhotos
from hass_sleep_camera.messages.stop_photos import StopPhotos
from hass_sleep_camera.settings import settings

if __name__ == '__main__':
    now = datetime.now()
    dt_string = now.strftime("%Y_%m_%d__%H_%M_%S")
    curr_folder = pathlib.Path(__file__).parent.absolute()

    logging.basicConfig(
        filename=f'{curr_folder}/logs/{dt_string}.log',
        filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.DEBUG)

    camera_controller = CameraController()

    MESSAGES = [StartPhotos(), StopPhotos()]
    message_manager = MessageManager(MESSAGES)
    message_manager.update_credentials(settings.USERNAME,
                                       settings.PASSWORD)
    message_manager.connect(settings.ADDRESS, settings.PORT)

    logging.info('Starting message manager')
    message_manager.start()

    try:
        message_manager.loop_forever()
    except KeyboardInterrupt:
        message_manager.stop()
        camera_controller.stop()

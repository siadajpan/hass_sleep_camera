import os

DELAY_BETWEEN_PHOTOS_S = 1  # photo done every n second
ROOT_FOLDER = '/home/pi/images'
SLEEP_FOLDER = os.path.join(ROOT_FOLDER, 'sleep')
PROJECT_FOLDER = os.path.abspath('../..')
HAAR_CASCADE_FOLDER = os.path.join(
    PROJECT_FOLDER, 'venv', 'lib', 'python3.8',
    'site-packages', 'cv2', 'data')
CAMERA_RESOLUTION = (2592, 1944)


class Mqtt:
    ADDRESS = '192.168.0.193'
    PORT = 1883
    USERNAME = 'karol'
    PASSWORD = 'klapeczki'
    TOPIC = 'camera/master_bedroom/bed/'
    ERROR_TOPIC = 'errors/camera/master_bedroom/bed/'


class Messages:
    START_PHOTOS = Mqtt.TOPIC + "start_photos"
    STOP_PHOTOS = Mqtt.TOPIC + "stop_photos"
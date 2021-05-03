import os


class Mqtt:
    ADDRESS = '192.168.0.164'
    PORT = 1883
    USERNAME = 'karol'
    PASSWORD = 'klapeczki'
    TOPIC = 'camera/master_bedroom/bed/'
    ERROR_TOPIC = 'errors/camera/master_bedroom/bed/'


class Messages:
    START_PHOTOS = Mqtt.TOPIC + "start_photos"
    STOP_PHOTOS = Mqtt.TOPIC + "stop_photos"


class Timings:
    DELAY_BETWEEN_PHOTOS_S = 1  # photo done every second
    QUICK_PHOTOS_FREQUENCY = 1  # every photo will be saved
    SLOW_PHOTOS_FREQUENCY = 10  # every tenth photo will be saved
    AMOUNT_QUICK_PHOTOS = 10
    QUEUE_SIZE_S = 60  # images saved after this amount of s


class Folders:
    ROOT_FOLDER = '/home/pi/images'
    WAKE_UP_FOLDER = os.path.join(ROOT_FOLDER, 'wake_up')
    SLEEP_FOLDER = os.path.join(ROOT_FOLDER, 'sleep')


class Inputs:
    BUTTON_NUMBER = 17

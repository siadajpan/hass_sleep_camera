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
    QUICK_PHOTOS_DELAY = 10
    SLOW_PHOTOS_DELAY = 60
    AMOUNT_QUICK_PHOTOS = 100

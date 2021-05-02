class PhotosCounter:
    def __init__(self, reset_callable):
        self._amount_of_photo_left = 0
        self.reset_callable = reset_callable

    def update_photos_left(self, amount_of_photos_left):
        self._amount_of_photo_left = amount_of_photos_left

    def update_photo_counter(self):
        self._amount_of_photo_left -= 1

    def counter_done(self):
        return self._amount_of_photo_left <= 0

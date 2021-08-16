import time
from unittest import TestCase
from unittest.mock import MagicMock, call, patch

import cv2
import numpy as np

from hass_sleep_camera.photo_managers.photos_queue import PhotosQueue


class TestPhotoQueue(TestCase):
    def setUp(self) -> None:
        self.photo_queue = PhotosQueue('saving_folder')

    def tearDown(self) -> None:
        self.photo_queue.stop()

    def test_can_be_started_and_stopped(self):
        # given
        self.photo_queue.start()

        # when
        self.photo_queue.stop()

        # then it's not hanging
        self.assertTrue(True)

    def test_can_add_photo(self):
        # given
        self.photo_queue.save_photo = MagicMock()
        self.photo_queue._lock = MagicMock()
        self.photo_queue._lock.acquire = MagicMock()
        self.photo_queue._queue_size_s = 1
        photo = MagicMock()
        time_now = time.time()
        self.photo_queue.start()

        # when
        self.photo_queue._photos_queue.put((time_now, photo))

        # then
        time.sleep(0.001)
        call_args = self.photo_queue._lock.acquire.call_args_list[0].kwargs
        self.assertAlmostEqual(1, call_args['timeout'], places=2)
        self.photo_queue.save_photo.assert_called()

    @patch('cv2.imwrite')
    def test_skipping_saving_photos(self, imwrite_mock):
        # given
        self.photo_queue._saving_frequency = 3
        self.photo_queue._saving_folder = 'saving_folder'
        photo = MagicMock()

        # when
        for i in range(3):
            self.photo_queue.save_photo(photo, str(i))

        path, photo_save = imwrite_mock.call_args_list[0].args
        self.assertEqual('saving_folder/2.jpg', path)
        self.assertEqual(photo, photo_save)

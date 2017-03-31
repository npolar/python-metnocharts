import unittest

from metnocharts.utils import get_timestamp_from_filename
import numpy as np

class TestMetChartsUtils(unittest.TestCase):

    def test_get_timestamp_from_filename(self):
        metchart_basename = 'ice20150401.shp'
        expected_timestamp = 5569
        timestamp = get_timestamp_from_filename(metchart_basename)
        self.assertEqual(expected_timestamp, timestamp)

    def test_timestamp_is_integer(self):
        metchart_basename = 'ice20150401.shp'
        timestamp = get_timestamp_from_filename(metchart_basename)
        self.assertIsInstance(timestamp, np.uint16)

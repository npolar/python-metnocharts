import numpy as np
import os
import unittest
from rasterio import features
import rasterio
from metnocharts import charts

class TestCharts(unittest.TestCase):

    def setUp(self):
        ifile = 'test_data/ice20150401.npy'
        shp_file = 'test_data/ice20150401.shp'
        self.geotransform = charts.IceChartDataset(shp_file).setup_geotransform()
        self.ifile = ifile
        self.assertTrue(os.path.exists(ifile))
        dst = np.load(ifile)
        self.dst = dst
        self.assertIsInstance(dst, np.ndarray)
        self.shape_gen = features.shapes(dst, transform=self.geotransform)
        self.crs=charts.get_crs()

    def test_polygonize_raster_fastice(self):
        self.assertIsInstance(len(list(self.shape_gen)),int)

    def test_rasterize_shapes(self):
        rdst = features.rasterize(shapes=self.shape_gen,
                                  out_shape=self.dst.shape)
        self.assertEquals(rdst.sum(), self.dst.sum())

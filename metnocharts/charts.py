import numpy as np
import netCDF4 as nc
import geopandas as gpd
import rasterio
from rasterio import features
from rasterio import transform

from metnocharts.utils import get_timestamp_from_filename


class IceChartDataset(object):
    def __init__(self, fname):
        self.fname = fname
        self.read_dst(fname)
        self.setup_geotransform()
        self.ice_conc = None
        self.shapes = None
        self.crs = get_crs()

    def setup_geotransform(self):
        self.xres = 100
        self.yres = 100
        self.west    =  225000
        self.north   = -970000
        self.south   = -1450000
        self.east    =  570000
        self.height = (abs(self.south - self.north) + self.yres)/self.yres
        self.width  = (abs(self.east - self.west) + self.xres)/self.xres

        self.geotransform = transform.from_origin(self.west-self.xres/2,
                                               self.north+self.xres/2,
                                               self.xres,
                                               self.yres)

    def rasterize(self):
        if self.shapes is None:
            self.read_shp()

        self.shapes['Value']=1
        self.shapes.crs = {'init':'epsg:4326'}
        self.shapes.to_crs(self.crs)
        shapes = ((geom,value) for geom, value in zip(self.shapes.geometry,
                                                        self.shapes['Value']))
        self.ice_conc = features.rasterize(shapes=shapes,
                                           out_shape=(self.height, self.width),
                                           fill=0,
                                           transform=self.geotransform)

    def save_netcdf(self, fname):
        if self.ice_conc is not None:
            nc_filehandle = self.create_netcdf_chart(fname)
            nc_filehandle['ice_concentration'][0,:,:] = self.ice_conc
            nc_filehandle['time'][:] = self.timestamp
            nc_filehandle.close()

    def make_geotiff_profile(self):
        profile = {'driver': 'GTiff',
                   'crs': self.crs,
                   'compress': 'lzw',
                   'dtype': 'uint8',
                   'interleave': 'band',
                   'count': 1,
                   'transform': self.geotransform,
                   'height': self.height,
                   'width': self.width}
        return profile

    def save_geotiff(self, fname):
        profile = self.make_geotiff_profile()
        if self.ice_conc is not None:
            with rasterio.open(fname, 'w', **profile) as dst:
                dst.write(self.ice_conc.astype(rasterio.uint8), 1)
        else:
            raise Exception('No ice concentration array available')

    def read_dst(self, fname):
        self.timestamp = get_timestamp_from_filename(self.fname)
        self.read_shp()

    def read_shp(self):
        shp_dst = gpd.read_file(self.fname)
        shp_dst = shp_dst.loc[shp_dst['ICE_TYPE'] == 'Fast Ice']
        self.shapes = shp_dst

    def create_netcdf_chart(self, fname):
        """Create a netCDF file"""
        root_dst = nc.Dataset(fname, 'w', format='NETCDF4')
        if self.crs is not None:
            root_dst.crs = self.crs
        root_dst.x_upper_left = self.west
        root_dst.y_upper_left = self.north

        # create dimensions, we assume the data is always 3d
        root_dst.createDimension('time', None)
        root_dst.createDimension('y', self.height)
        root_dst.createDimension('x', self.width)

        # create variables
        root_dst.createVariable('time',
                                'i4',
                                dimensions=('time'))
        root_dst.createVariable('ice_concentration',
                                'i4',
                                dimensions=('time', 'y', 'x'),
                                zlib=True)
        root_dst.variables['time'].units = 'Days since 2000-01-01'
        return root_dst

def get_crs():
    crs = '+proj=stere +lat_0=90 +lat_ts=90 +lon_0=0 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs'
    return crs

def get_fastice_from_chart(fname):
    fastice_dst = IceChartDataset(fname)
    return fastice_dst

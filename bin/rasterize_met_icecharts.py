#!/usr/bin/env python

import argparse

import geopandas as gpd
import rasterio
import fiona
from rasterio import features
import os
from datetime import datetime as dt
from rasterio.transform import from_origin
import netCDF4 as nc
from netCDF4 import netcdftime
from netcdftime import utime

class GeoTIFFTemplate(object):
    def __init__(self):
        self.res = 100
        self.west    =  225000
        self.north   = -970000
        self.south   = -1450000
        self.east    =  570000
        self.height = (abs(self.south - self.north) + self.res)/self.res
        self.width = (abs(self.east - self.west) + self.res)/self.res
        self.crs = '+proj=stere +lat_0=90 +lat_ts=90 +lon_0=0 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs'
        self.transform = from_origin(self.west - self.res/2,
                                     self.north+self.res/2, self.res, self.res)
        self.shape = (self.height, self.width)
 

def rasterize_layer(convert_to_rast, rst, field, shape=None):
    # this is where we create a generator of geom, value pairs to use in rasterizing
    shapes = ((geom,value) for geom, value in zip(convert_to_rast.geometry, convert_to_rast[field]))
    burned = features.rasterize(shapes=shapes, fill=0, out_shape=shape, transform=rst.transform)
    return burned
                
def create_netcdf_file(fname, shape, crs=None, north=None, west=None):
    """Create a netCDF file with variable dimensions *shape*
    Args:
      fname (str) : output filename
      shape (tuple) : data array dimensions
    Returns:
      root_dst (netCDF4.Dataset)  : dataset open for writing
    """
    root_dst = nc.Dataset(fname, 'w', format='NETCDF4')
    if crs is not None:
        root_dst.crs = crs
    root_dst.x_upper_left = west
    root_dst.y_upper_left = north

    # create dimensions, we assume the data is always 3d
    root_dst.createDimension('time', None)
    root_dst.createDimension('y', shape[1])
    root_dst.createDimension('x', shape[0])
    
    # create variables
    root_dst.createVariable('time', 'i4', 
                            dimensions=('time'))
    root_dst.createVariable('ice_concentration', 'i4', 
                            dimensions=('time', 'x', 'y'),
                            zlib=True)
    root_dst.variables['time'].units = 'Days since 2000-01-01'
    return root_dst

def get_timestamp_from_filename(fname):
    '''Parse basename and return cdf time'''
    date = dt.strptime(fname, 'ice%Y%m%d.shp')
    cdftime = utime('days since 2000-01-01')
    timestamp = cdftime.date2num(date)
    return timestamp


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ifile", "-i")
    parser.add_argument("--ofile", "-o")
    parser.add_argument("--template", "-t")
    args = parser.parse_args()

    ifile = args.ifile
    ofile = args.ofile
    tif_template = args.template

    rst = rasterio.open(tif_template)
    convert_to_rast = gpd.read_file(ifile) 
    convert_to_rast = convert_to_rast.loc[convert_to_rast['ICE_TYPE'] == 'Fast Ice']
    convert_to_rast['Junk'] = 1    
    if rst.crs != convert_to_rast.crs:
         convert_to_rast = convert_to_rast.to_crs(rst.crs)
    template = GeoTIFFTemplate()
    data = rasterize_layer(convert_to_rast, rst, 'Junk', shape=template.shape)
    out_dst = create_netcdf_file(ofile, data.shape, crs=template.crs,
            west=template.west, north=template.north)
    out_dst.variables['time'][:] = timestamp 
    out_dst.variables['ice_concentration'][0,:,:] = data 

    out_dst.close()

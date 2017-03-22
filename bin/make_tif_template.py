#!/usr/bin/env python

import rasterio
import fiona
import numpy as np

from rasterio.transform import from_origin

def create_template_tif():
    '''Create template file for Svalbard area for use with new rasters'''
    output_fname = 'svalbard_template.tif'
    res     =  100 # 100 meters spatial resolution
    west    =  225000
    north   = -970000
    south   = -1450000
    east    =  570000
    height = (abs(south - north) + res)/res
    width = (abs(east - west) + res)/res

    crs = '+proj=stere +lat_0=90 +lat_ts=90 +lon_0=0 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs'

    profile = {'driver': 'GTiff',
                'height': height, 'width': width,
                'count': 1,
                'dtype': rasterio.ubyte,
                'compress': 'lzw',
                'crs': crs}

    transform = from_origin(west - res/2, north+res/2,  res, res)

    new_dst = rasterio.open(output_fname,
                            'w',
                            transform=transform,
                            **profile)
    new_dst.close()

def main():
    create_template_tif()

if __name__ == '__main__':
    main()

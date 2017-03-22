import os
import numpy as np
from netcdftime import utime
from datetime import datetime as dt

def get_timestamp_from_filename(fname):
    '''Parse basename and return cdf time'''
    basename = os.path.basename(fname)
    date = dt.strptime(basename, 'ice%Y%m%d.shp')
    cdftime = utime('days since 2000-01-01')
    timestamp = cdftime.date2num(date)
    return timestamp.astype(np.uint16)

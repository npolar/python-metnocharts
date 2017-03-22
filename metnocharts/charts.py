import netCDF4 as nc
from metnocharts.utils import get_timestamp_from_filename

class IceChartDataset(object):
    def __init__(self, fname):
        self.fname = fname
        self.read_dst(fname)
    
    def rasterize(self):
        self.ice_conc = None

    def save_netcdf(self, fname):
        nc_filehandle = create_netcdf_chart(fname, self.crs)
        nc_filehandle['ice_concentration'][:] = self.ice_conc
        nc_filehandle['time'][:] = self.timestamp
        nc_filehandle.close()

    def read_dst(self, fname):
        self.timestamp = get_timestamp_from_filename(self.fname)
        self.crs = get_crs(fname)
        self.read_shp()

    def read_shp(self):
        pass

def get_crs(fname):
    crs = '+proj=stere +lat_0=90 +lat_ts=90 +lon_0=0 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs'
    return crs

def get_fastice_from_chart(fname):
    fastice_dst = IceChartDataset(fname)
    return fastice_dst

def create_netcdf_chart(fname, crs):
    """Create a netCDF file"""
    root_dst = nc.Dataset(fname, 'w', format='NETCDF4')
    if crs is not None:
        root_dst.crs = crs

    xres = 100
    yres = 100

    west    =  225000
    north   = -970000
    south   = -1450000
    east    =  570000

    height = (abs(south - north) + yres)/yres
    width = (abs(east - west) + xres)/xres

    root_dst.x_upper_left = west
    root_dst.y_upper_left = north

    # create dimensions, we assume the data is always 3d
    root_dst.createDimension('time', None)
    root_dst.createDimension('y', height)
    root_dst.createDimension('x', width)
    
    # create variables
    root_dst.createVariable('time', 'i4', 
                            dimensions=('time'))
    root_dst.createVariable('ice_concentration', 'i4', 
                            dimensions=('time', 'x', 'y'),
                            zlib=True)
    root_dst.variables['time'].units = 'Days since 2000-01-01'
    return root_dst

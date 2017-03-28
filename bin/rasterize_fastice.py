#!/usr/bin/env python

import argparse
from metnocharts.charts import get_fastice_from_chart

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--ifile", "-i")
    parser.add_argument("--ofile", "-o")
    args = parser.parse_args()

    ifile = args.ifile
    ofile = args.ofile

    fastice_dst = get_fastice_from_chart(ifile)
    fastice_dst.rasterize()
    fastice_dst.save_netcdf(ofile)

if __name__ == '__main__':
    main()

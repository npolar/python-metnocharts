#!/usr/bin/env python

import argparse
from metnocharts.charts import get_fastice_from_chart
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--ifile", "-i")
    parser.add_argument("--ofile", "-o")
    args = parser.parse_args()

    ifile = args.ifile
    ofile = args.ofile

    fastice_dst = get_fastice_from_chart(ifile)
    fastice_dst.rasterize()
    fastice_dst.save_geotiff(ofile)

if __name__ == '__main__':
    main()

#!/usr/bin/env python

from fabric.operations import local as run
from fabric.api import execute, hosts
from fabric.state import env

import os
import logging

logging.basicConfig(filename='example.log',level=logging.DEBUG)

def get_data(ofile, dirname=None):
    run("wget https://www.dropbox.com/s/x3bj0rjf0ectml6/icechart-20150401.zip?dl=1 -O {}".format(ofile))
    run('unzip {} -d {}'.format(ofile, dirname))
    try:
        os.remove(ofile)
        logging.info('Removed file {}'.format(ofile))
    except:
        raise IOError

hosts = ['localhost']
execute(get_data, 'o.zip', dirname='test_data', hosts=hosts)

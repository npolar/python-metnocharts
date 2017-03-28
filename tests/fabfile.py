from fabric.operations import local as run
from fabric.api import execute, hosts
from fabric.state import env

def get_data(ofile, dirname=None):
    run("wget https://www.dropbox.com/s/x3bj0rjf0ectml6/icechart-20150401.zip?dl=1 -O {}".format(ofile))
    run('unzip {} -d {}'.format(ofile, dirname))

hosts = ['localhost']
execute(get_data, 'o.zip', dirname='test_data', hosts=hosts)

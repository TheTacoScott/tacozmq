#!/usr/bin/env python

"""
TacoNET: darknet written in python and zeromq

Author: Scott Powers
"""

import sys
import argparse
import zmq
import json
import taco.bottle
import taco.constants
import taco.server
import taco.dispatch
import taco.crypto
import taco.settings

if __name__ == '__main__':
  if zmq.zmq_version_info() < (4,0):
    raise RuntimeError("Security is not supported in libzmq version < 4.0. libzmq version {0}".format(zmq.zmq_version()))
  if sys.version_info < (2, 6, 5):
    raise RuntimeError("must use python 2.6.6 or greater")
  
parser = argparse.ArgumentParser(description='TacoNET: a darknet written in python and zeromq')
parser.add_argument('--config', default=taco.constants.JSON_SETTINGS_FILENAME,dest='configfile',help='specify the location of the config json')
args = parser.parse_args()

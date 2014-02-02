#!/usr/bin/env python

"""
TacoNET: darknet written in python and zeromq

Author: Scott Powers
"""

import sys
import argparse
import zmq
import json
import logging

import taco.bottle
import taco.constants
import taco.server
import taco.dispatch
import taco.crypto
import taco.settings

if zmq.zmq_version_info() < (4,0):
  raise RuntimeError("Security is not supported in libzmq version < 4.0. libzmq version {0}".format(zmq.zmq_version()))
if sys.version_info < (2, 6, 5):
  raise RuntimeError("must use python 2.6.6 or greater")
  
parser = argparse.ArgumentParser(description='TacoNET: a darknet written in python and zeromq')
parser.add_argument('--config', default=taco.constants.JSON_SETTINGS_FILENAME,dest='configfile',help='specify the location of the config json')
parser.add_argument("--verbose", default=False,dest="verbose",help="increase output verbosity",action="store_true")
parser.add_argument("--debug", default=False,dest="debug",help="increase output verbosity to an insane level",action="store_true")
args = parser.parse_args()

level = logging.ERROR
if args.verbose == True: level = logging.INFO
if args.debug == True: level = logging.DEBUG
logging.basicConfig(level=level, format="[%(levelname)s]\t[%(asctime)s] - %(filename)s:%(lineno)d\t%(funcName)s:\t%(message)s")

taco.settings.Load_Settings()

#!/usr/bin/env python

import lyftplan
from importlib import import_module

import sys
import os

#
# App
#
def main():
    if len(sys.argv) < 2 or not os.path.isdir(sys.argv[1]):
        print("usage: {} folder".format(sys.argv[0]))
        sys.exit(1)

    lifter = sys.argv[1]

    bank = import_module('{}.bank'.format(lifter))
    lyftplan.register(bank)

    program = import_module('{}.program'.format(lifter))
    program.main()

if __name__ == '__main__':
    main()



#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

filename = sys.argv[1]
# print(filename)

cpu = CPU()

cpu.load(filename)
cpu.run()

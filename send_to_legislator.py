#!/usr/bin/env python
# -*- coding: utf-8 -*-

# run command line program as 'python send_to_legislator file_name.txt'

import sys

lines = []
input_info = {}

# input_legend = {
    
# }

# input read in as a file
# f = open(sys.argv[1], "r")

with open(sys.argv[1], "r") as f:
    # for line in f:
    #     print "begin " + line + " end."
    # list of values (strings) with \n\r return-newline removed
    lines = f.read().splitlines()

print lines

for line in lines:
    val = line.split(':')
    input_info[val[0]] = val[1].strip()

print input_info


# assumes that all files formatted the same, like sample content
# create a 
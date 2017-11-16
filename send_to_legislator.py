#!/usr/bin/env python
# -*- coding: utf-8 -*-

# run command line program as 'python send_to_legislator file_name.txt'

import sys
import os

lines = []
input_info = {}
input_key_legend = {
    "From Name": "from_name",
    "From Address Line 1": "from_address_line_1",
    "From Address Line 2": "from_address_line_2",
    "From City": "from_city",
    "From Country": "from_country",
    "From Zip Code": "from_zip_code",
    "Message": "message"
}
google_civic_key = os.environ['GOOGLE_CIVIC_KEY']

# open and read input file
with open(sys.argv[1], "r") as f:
    # list of values (strings) with \n\r return-newline removed
    lines = f.read().splitlines()
# print lines

for line in lines:
    data = line.split(':')

    if data[0] in input_key_legend:
        input_key = input_key_legend[data[0]]
        print "yes!"
    else:
        input_key = data[0].lower().replace(" ", "_")
    # print input_key

    input_val = data[1].strip()

    input_info[input_key] = input_val
# print input_info


# assumes that all files formatted the same, like sample content
# create a 
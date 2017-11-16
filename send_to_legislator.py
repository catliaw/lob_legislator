#!/usr/bin/env python
# -*- coding: utf-8 -*-

# run command line program as 'python send_to_legislator file_name.txt'

import sys
import os

from apiclient.discovery import build

google_civic_key = os.environ['GOOGLE_CIVIC_KEY']
lob_test_api_key = os.environ['LOB_TEST_API_KEY']

lines = []
input_info = {}
input_key_legend = {
    "From Name": "from_name",
    "From Address Line 1": "from_address_line_1",
    "From Address Line 2": "from_address_line_2",
    "From City": "from_city",
    "From State": "from_state",
    "From Country": "from_country",
    "From Zip Code": "from_zip_code",
    "Message": "message"
}

governor_info = {}

# open and read input file
with open(sys.argv[1], "r") as f:
    # list of values (strings) with \n\r return-newline removed
    lines = f.read().splitlines()
print lines

# from input file, read each line and parse info into input_info dictionary
for line in lines:
    data = line.split(':')

    if data[0] in input_key_legend:
        input_key = input_key_legend[data[0]]
        print "yes!"
    # else:
    #     # can raise an input error here, since key will not be correct
    #     input_key = data[0].lower().replace(" ", "_")
    print input_key

    input_val = data[1].strip()

    input_info[input_key] = input_val
print input_info

# new address string to input into Google Civic API as parameter later
input_info['complete_address'] = "%s %s %s %s %s" % (input_info["from_address_line_1"],
                                                     input_info["from_address_line_2"],
                                                     input_info["from_city"],
                                                     input_info["from_state"],
                                                     input_info["from_zip_code"])
print input_info['complete_address']


# Create a service object for the correct API, version, authentication key
service = build('civicinfo', 'v2', developerKey=google_civic_key)

# Format request with specified parameters
# 'administrativeArea1' means (in the USA) the state-level
# 'headOfGovernment' means the state governor
req = service.representatives().representativeInfoByAddress(address=input_info['complete_address'],
                                                            levels='administrativeArea1',
                                                            roles='headOfGovernment')

# Execute the request to get a response using execute function
civic_response = req.execute()

# Find state governor information
# Governor name is response['officials'][0]['name']
governor_info['name'] = civic_response['officials'][0]['name']
# Address is response['officials'][0]['address'][0]
# Keys are 'line1', 'line2', 'city', state', 'zip'
for key, value in civic_response['officials'][0]['address'][0].iteritems():
    governor_info[key] = value

print governor_info


# assumes that all files formatted the same, like sample content
# create a 
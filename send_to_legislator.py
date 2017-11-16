#!/usr/bin/env python
# -*- coding: utf-8 -*-

# run command line program as 'python send_to_legislator file_name.txt'

import sys
import os
import lob
from apiclient.discovery import build

google_civic_key = os.environ['GOOGLE_CIVIC_KEY']
lob.api_key = os.environ['LOB_TEST_API_KEY']

lines = []
sender_info = {}
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

###########################################################################
# This command line tool allows one argument - a text file that is opened #
# and read. Each line then parsed into a Python dictionary (sender_info)  #
###########################################################################

# open and read input file
with open(sys.argv[1], "r") as f:
    # list of values (strings) with \n\r return-newline removed
    lines = f.read().splitlines()

# from input file, read each line and parse info into sender_info dictionary
for line in lines:
    data = line.split(':')

    # assumes that all input files formatted the same, like sample content
    if data[0] in input_key_legend:
        input_key = input_key_legend[data[0]]
    else:
        # can raise an input error here, since key will not be correct
        exception_message = "%s input label is not correct. Correct input labels \
are From Name, From Address Line 1,\nFrom Address Line 2,From City, From State, \
From Country, From Zip Code, and Message." % (data[0])
        raise Exception(exception_message)

    input_val = data[1].strip()

    sender_info[input_key] = input_val

# new address string to input into Google Civic API as parameter later
sender_info['complete_address'] = "%s %s %s %s %s" % (sender_info["from_address_line_1"],
                                                      sender_info["from_address_line_2"],
                                                      sender_info["from_city"],
                                                      sender_info["from_state"],
                                                      sender_info["from_zip_code"])

###################################################################
# Using the Google Civic API and sender's address, find the local #
# legislator info (specified to state governor in this function). #
###################################################################

# Create a service object for the correct API, version, authentication key
service = build('civicinfo', 'v2', developerKey=google_civic_key)

# Format request with specified parameters
# 'administrativeArea1' means (in the USA) the state-level
# 'headOfGovernment' means the state governor
req = service.representatives().representativeInfoByAddress(address=sender_info['complete_address'],
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

##########################################################################
# Using Lob API, create a letter with sender's name/address,             # 
# governor's name/address, and message to governor (500 character limit) #
##########################################################################

# Create a Lob Address object for the sender
sender_address = lob.Address.create(
    name=sender_info["from_name"],
    address_line1=sender_info["from_address_line_1"],
    address_line2=sender_info["from_address_line_2"],
    address_city=sender_info["from_city"],
    address_state=sender_info["from_state"],
    address_zip=sender_info["from_zip_code"]
)

# Create a Lob Address object for the governor (legislator)
# Ran into some issue with the governor's address and minimum deliverability
# strictness, so switched US Mail Strictness setting to 'Relaxed'.
# Cannot change what Google Civic API gives us as the legislator address.
# If had more time, maybe could use Google Map API to find alternate address.
governor_address = lob.Address.create(
    name=governor_info["name"],
    address_line1=governor_info["line1"],
    address_line2=governor_info["line2"],
    address_city=governor_info["city"],
    address_state=governor_info["state"],
    address_zip=governor_info["zip"]
)

letter_to_governor = lob.Letter.create(
    description='Letter to Governor',
    to_address=governor_address,
    from_address=sender_address,
    address_placement='top_first_page',
    file="""
        <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet" type="text/css">
        <title>Letter to Governor</title>
        <style>
          *, *:before, *:after {
            -webkit-box-sizing: border-box;
            -moz-box-sizing: border-box;
            box-sizing: border-box;
          }
          body {
            width: 8.5in;
            height: 11in;
            margin: 0;
            padding: 0;
            background-color: rgba(0,0,0,0);
          }
          .page {
            page-break-after: always;
            position: relative;
            width: 8.5in;
            height: 11in;
          }
          .page-content {
            position: absolute;
            width: 8.125in;
            height: 10.625in;
            left: 0.1875in;
            top: 0.1875in;
          }
          .text {
            position: relative;
            left: .4375in;
            top: 20px;
            width: 6in;
            font-family: 'Open Sans';
            font-size: 16px;
          }
        </style>
        </head>
        <body>
          <div class="page">
            <div class="page-content">
              <div class="text" style="top: 3in;">
                {{message}}
              </div>
            </div>
          </div>
        </body>
        </html>""",
    merge_variables={
        'message': sender_info['message']
    },
    color=False
)

print letter_to_governor
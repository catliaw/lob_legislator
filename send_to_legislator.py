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
print lines

# from input file, read each line and parse info into sender_info dictionary
for line in lines:
    data = line.split(':')

    # assumes that all input files formatted the same, like sample content
    if data[0] in input_key_legend:
        input_key = input_key_legend[data[0]]
        print "yes!"
    # else:
    #     # can raise an input error here, since key will not be correct
    #     input_key = data[0].lower().replace(" ", "_")
    print input_key

    input_val = data[1].strip()

    sender_info[input_key] = input_val
print sender_info
print sender_info['message']

# new address string to input into Google Civic API as parameter later
sender_info['complete_address'] = "%s %s %s %s %s" % (sender_info["from_address_line_1"],
                                                      sender_info["from_address_line_2"],
                                                      sender_info["from_city"],
                                                      sender_info["from_state"],
                                                      sender_info["from_zip_code"])
print sender_info['complete_address']


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

print governor_info

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
print sender_address

# Create a Lob Address object for the governor (legislator)
governor_address = lob.Address.create(
    name=governor_info["name"],
    address_line1=governor_info["line1"],
    address_line2=governor_info["line2"],
    address_city=governor_info["city"],
    address_state=governor_info["state"],
    address_zip=governor_info["zip"]
)
print governor_address

# letter_to_governor = lob.Letter.create(
#     description='Letter to Governor',
#     to_address=governor_address,
#     from_address=sender_address,
#     file="""
#       <html>
#         <head>
#           <style>
#             @font-face {
#               font-family: 'Loved by the King';
#               src: url('https://s3-us-west-2.amazonaws.com/lob-assets/LovedbytheKing.ttf');
#             }
#           </style>
#         </head>
#         <body><h1>Special offer for {{message}}</h1></body>
#       </html>""",
#     merge_variables={
#         'message': sender_info['message']
#     },
#     color=False
# )

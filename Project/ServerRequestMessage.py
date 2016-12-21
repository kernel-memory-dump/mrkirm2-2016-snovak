#############################################################################
#
#
#
# DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                 Version 2, December 2004
#
#      Everyone is permitted to copy and distribute verbatim or modified
#      copies of this license document, and changing it is allowed as long
#      as the name is changed.
#
#         DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE,
#         TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#         0. You just DO WHAT THE FUCK YOU WANT TO
#
#  -----------------------------------------------------
#  Sebastian Novak @ GitHub https://github.com/kernel-memory-dump
#  -----------------------------------------------------
#
#
# @author  Sebastian Novak
#
#
#############################################################################

import json

class ServerRequestMessage:

    def __init__(self, json_data=None):
        self.__input_bucket_name = None
        self.__input_bucket_key = None
        if json_data is not None:
            self.__parse_json_data(json_data)

    def __parse_json_data(self, data):
        parsed = json.loads(data)
        self.__input_file_url = parsed["input_file_url"]

    def set_input_file_bucket_name(self, bucket_name):
        self.__input_bucket_name = bucket_name

    def get_input_file_bucket_name(self):
        return self.__input_bucket_name

    def set_input_file_bucket_key(self, bucket_name):
        self.__input_bucket_name = bucket_name

    def get_input_file_bucket_key(self):
        return self.__input_bucket_name



    def as_json_str(self):
        return json.dumps({"input_file_url":self.__input_file_url})

    def as_str(self):
        return "input_file:" + str(self.__input_file_url)

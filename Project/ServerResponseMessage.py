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


class ServerResponseMessage:
    """Object representation of a response_queue message body"""
    def __init__(self, json_data=None):
        self.__output_file_url = None
        # indicates if request was processed properly
        # if false, processing failed and there is no valid output
        self.__successful = False
        if json_data is not None:
            self.__parse_json_data(json_data)

    def __parse_json_data(self, data):
        parsed = json.loads(data)
        self.__output_file_url = parsed["output_file_url"]
        self.__successful = parsed["successful"]

    def set_output_file_url(self, url):
        self.__output_file_url = url

    def get_output_file_url(self):
        return self.__output_file_url

    def is_successful(self):
        return self.__successful

    def set_successful(self, value):
        self.__successful = value

    def as_json_str(self):
        return json.dumps({"output_file_url":self.__output_file_url, "successful": self.__successful})

    def as_str(self):
        return "output_file:" + str(self.__output_file_url) + " successful:" + str(self.__successful)


class ResponseEntity:
    """Object representation of JSON placed in the output bucket"""
    def __init__(self, keyword_count=0, json_data=None):
        self.__keyword_count = keyword_count
        if json_data is not None:
            self.__parse_json_data(json_data)

    def __parse_json_data(self, data):
        parsed = json.loads(data)
        self.__keyword_count = parsed["keyword_count"]

    def as_json_str(self):
        return json.dumps({"keyword_count":self.__keyword_count})

    def get_keyword_count(self):
        return self.__keyword_count

    def set_keyword_count(self, value):
        self.__keyword_count = value

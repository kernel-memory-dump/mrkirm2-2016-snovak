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
from pprint import pprint
from S3Handler import S3Handler
import os


CONFIG_JSON_BUCKET = "snovak.project.bucket"
CONFIG_JSON_KEY = "config.json"

def acquire_config():
    config_bucket_handler = S3Handler(CONFIG_JSON_BUCKET)
    config_bucket_handler.download_file(CONFIG_JSON_KEY, CONFIG_JSON_KEY)
    config = Config("config.json")
    return config


class Config:
    def __init__(self, json_path):
        self.json_path = json_path
        self.__data = {}
        self.load()

    def load(self):
        with open(self.json_path) as data_file:
            self.__data = json.load(data_file)

    def print_config(self):
        print("Input bucket name:" + self.get_input_bucket_name())
        print("Output bucket name:" + self.get_output_bucket_name())
        print("Request queue name:" + self.get_request_queue_name())
        print("Response queue  name:" + self.get_response_queue_name())
        print("Status:" + self.get_status())
        print("Server instance ID:" + self.get_server_id())

    def get_status(self):
        return self.__data["status"]

    def set_status(self, value):
        self.__data["status"] = value

    def get_input_bucket_name(self):
        return self.__data["input_bucket_name"]

    def get_output_bucket_name(self):
        return self.__data["output_bucket_name"]

    def get_request_queue_name(self):
        return self.__data["request_queue_name"]

    def get_response_queue_name(self):
        return self.__data["response_queue_name"]

    def get_server_id(self):
        return self.__data["server_id"]

    def set_server_id(self, value):
        """ EC2 instance id required for performing clean-up"""
        self.__data["server_id"] = value

    def update(self):
        """ Updates config.json on S3 using current Config object state"""
        config_file = open(CONFIG_JSON_KEY, 'w')
        config_file.write(self.as_json_str())
        config_file.close()


        config_bucket_handler = S3Handler(CONFIG_JSON_BUCKET)
        config_bucket_handler.upload_file(CONFIG_JSON_KEY, CONFIG_JSON_KEY, public=True)
        #os.remove(CONFIG_JSON_KEY)


    def as_json_str(self):
        return json.dumps(self.__data, indent=4, sort_keys=True)
#!/usr/bin/python3

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


import sys

from S3Handler import S3Handler
from SQSHandler import SQSHandler
from SQSHandler import SQSMessage
from ServerRequestMessage import ServerRequestMessage
from ServerResponseMessage import ServerResponseMessage

from Config import *
from Config import Config
from log import * 

def generate_client_id():
    """ Generates a client id with prefix snovak.client.'

    Args:
        None
    Returns:
        (str) - newly generated client id

    """

    from time import time
    return "snovak.client." + str(time())

def main():

    # Parse input arguments

    input_file = "test-file.txt"

    # load config
    config = acquire_config()
    config.print_config()

    # generate client id
    client_id = generate_client_id()

    file_key =  client_id + "__" + input_file

    # place input file inside input bucket
    #s3_input_handle = S3Handler(config.get_input_bucket_name())
    EXISTING_BUCKET_NAME = "snovak.public.input.bucket.2016.1234567890"
    s3_input_handle =  S3Handler(EXISTING_BUCKET_NAME)
    s3_input_handle.create_new_public_bucket()

    # place file under key client-id+__nput_file_name
    s3_input_handle.upload_file(input_file, file_url)

    # send command to request queue
    sqs_request_handle = SQSHandler(config.get_request_queue_name())
    sqs_request_msg = SQSMessage()
    sqs_request_msg.set_id(client_id)
    ################################################
    request_msg = ServerRequestMessage()

    request_msg.set_input_file_bucket_name(EXISTING_BUCKET_NAME)
    request_msg.set_input_file_bucket_key(file_key)

    sqs_request_msg.set_message_body(request_msg.as_json_str())
    ###############################################

    # send request to server to process uploaded file
    sqs_request_handle.send_message(sqs_request_msg)

    sqs_response_handle = SQSHandler(config.get_response_queue_name())

    s3_output_handle = S3Handler(config.get_output_bucket_name())

    # wait until response queue contains message with id set to client-id
    while True:
        sqs_response_handle.receive_messages()
        sqs_messages = sqs_response_handle.get_inbox().get_messages()
        sqs_response_handle.get_inbox().clear()
  
        for sqs_message in sqs_messages:
            #print(str(sqs_message.get_message_body))
            if sqs_message.get_id() != None and sqs_message.get_id() == client_id:
                print("Received my  response from server!")
                sqs_message.delete()
                # parse into object 
                response_msg = ServerResponseMessage(sqs_message.get_message_body())
                s3_output_handle.download_file(response_msg.get_output_file_url(), "from_server_" + response_msg.get_output_file_url())
                write_to_log("Received response from server!")
                break





if __name__ == '__main__':
    main()
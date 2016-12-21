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


import threading
from SQSHandler import SQSHandler
from SQSHandler import SQSMessage
from S3Handler import S3Handler
from Config import Config
from Config import *
from ServerRequestMessage import ServerRequestMessage
from ServerResponseMessage import ServerResponseMessage
import json
from log import * 

config = None

def generate_temp_file_name():
    """ Generates a client id with prefix snovak.client.'

    Args:
        None
    Returns:
        (str) - newly generated client id

    """

    from time import time
    return "output_file.server." + str(time())


def fetch_input_file(request_msg):
    input_bucket_handler = S3Handler(request_msg.get_input_file_bucket_name())
    input_bucket_handler.download_file(request_msg.get_input_file_bucket_key(), generate_temp_file_name())

    return ""

def process_request(sqs_message):
    global config
    # extract/parse input JSON
    msg_body = sqs_message.get_message_body()
    client_id = sqs_message.get_id()
    server_request_message = ServerRequestMessage(msg_body)

    # pull input file via S3

    output_bucket_handler = S3Handler(config.get_output_bucket_name())

    write_to_log("Received message from client:")
    # process file
    request_msg = ServerRequestMessage(msg_body)
    
    output_file_url = client_id + "___output.json"
    output_bucket_handler.upload_file('log.txt', output_file_url)

    # create response output
    sqs_response_msg = SQSMessage()
    sqs_response_msg.set_id(client_id)
    response_msg = ServerResponseMessage()

    input_put_file_url = request_msg.get_input_file_url()
    input_file_content = fetch_input_file(request_msg)

    response_msg.set_output_file_url(output_file_url)
    #############################################
    sqs_response_msg.set_message_body(response_msg.as_json_str())
    # upload response to output bucket under client_id_output_file_timestamp key
    # output_bucket_handler.upload_file('output-cid.json', 'output-cid_timestamp.json')

    sqs_response_handler = SQSHandler(config.get_response_queue_name())
    
    # send message to response queue using client_id as  msg-id
    sqs_response_handler.send_message(sqs_response_msg)

    


def main():

    global config
    # load config
    config = acquire_config()

    sqs_request_handle = SQSHandler(config.get_request_queue_name(), 5)

    while True:
        sqs_request_handle.receive_messages()
        sqs_messages = sqs_request_handle.get_inbox().get_messages()
        # clear inbox
        sqs_request_handle.get_inbox().clear()
        # process each request and dispatch a response
        for sqs_message in sqs_messages:
            process_request(sqs_message)

if __name__ == '__main__':
    main()
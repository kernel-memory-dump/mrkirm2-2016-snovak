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
from ServerResponseMessage import ResponseEntity
import json
from log import *
import os
import sys

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
    try:
        input_bucket_handler = S3Handler(request_msg.get_input_file_bucket_name())
        tmp_file_name = generate_temp_file_name()
        input_bucket_handler.download_file(request_msg.get_input_file_bucket_key(), tmp_file_name)
        input_file = open(tmp_file_name, "r")
        # read whole file as string
        file_content = input_file.read()
        # clean up tmp file
        input_file.close()
        os.remove(tmp_file_name)
        return file_content
    except:
        print("fetch_input_file failed!")
        print("Exception type:", str(sys.exc_info()[0]))
        print("Exception info:", str(sys.exc_info()[1]))
        return None


def count_keyword(content, keyword):
    return content.count(keyword)

def process_file_content(request_msg, response_msg,  client_id, input_file_content):
    ###########################################
    ## acquire input file content

    count_found = count_keyword(input_file_content, request_msg.get_keyword())

    # construct output file
    output_file_url = client_id + "___output.json"
    response_entity = ResponseEntity(keyword_count=count_found)
    tmp_file = open(output_file_url, 'w')
    tmp_file.write(response_entity.as_json_str())
    tmp_file.close()

    # upload response to output bucket under client_id_output_file_timestamp key
    output_bucket_handler = S3Handler(config.get_output_bucket_name())
    output_bucket_handler.create_new_public_bucket()
    output_bucket_handler.upload_file(output_file_url, output_file_url)
    os.remove(output_file_url)
    response_msg.set_output_file_url(output_file_url)


def process_request(sqs_message):

    global config
    # extract/parse input JSON
    msg_body = sqs_message.get_message_body()
    client_id = sqs_message.get_id()
    write_to_log("Received message from client:" + msg_body)
    print("processing message from client_id:" + client_id)

    # transform request body into object
    request_msg = ServerRequestMessage(msg_body)

    # create response output
    sqs_response_msg = SQSMessage()
    sqs_response_msg.set_id(client_id)
    response_msg = ServerResponseMessage()

    # process file, if valid, otherwise client will receive response message with successful set to False
    input_file_content = fetch_input_file(request_msg)
    if input_file_content != None:
        process_file_content(request_msg, response_msg, client_id, input_file_content)
        response_msg.set_successful(True)

    #############################################
    # SEND RESPONSE via SQS
    sqs_response_msg.set_message_body(response_msg.as_json_str())

    sqs_response_handler = SQSHandler(config.get_response_queue_name())
    
    # send message to response queue using client_id as  msg-id
    sqs_response_handler.send_message(sqs_response_msg)
    # mark as processed
    sqs_message.delete()


def main():

    global config
    # load config
    config = acquire_config()
    config.set_status("running")
    config.update()

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



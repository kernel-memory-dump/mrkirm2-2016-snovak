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



CONFIG_FILE_URL = "https://s3-us-west-2.amazonaws.com/snovak.project.bucket/config.json"
config = None

def write_to_log(line):
    log_file = open("log.txt", "a")
    from datetime import datetime
    time_part = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_file.write(time_part + ":" + line)
    log_file.close()

def process_request(self, sqs_message):
    global config
    # extract/parse input JSON
    msg_body = sqs_message.body
    client_id = sqs_message.get_id()
    server_request_message = ServerRequestMessage(msg_body)

    # pull input file via S3
    input_bucket_handler = S3Handler(config.get_input_bucket_name())
    output_bucket_handler = S3Handler(config.get_output_bucket_name())

    write_to_log("Received message from client:")
    # process file
    request_msg = ServerRequestMessage(msg_body)


    # create response output
    sqs_response_msg = SQSMessage()
    sqs_response_msg.set_id(client_id)
    response_msg = ServerResponseMessage()
    response_msg.set_output_file_url("lel")
    #############################################
    sqs_response_msg.set_message_body(response_msg.as_json_str())
    # upload response to output bucket under client_id_output_file_timestamp key
    # output_bucket_handler.upload_file('output-cid.json', 'output-cid_timestamp.json')

    sqs_response_handler = SQSHandler(config.get_response_queue_name())



    # send message to response queue using client_id as  msg-id
    sqs_response_handler.send_message(sqs_response_msg)

    


def main():

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
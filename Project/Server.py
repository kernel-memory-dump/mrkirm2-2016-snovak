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
from ServerRequestMessage import ServerRequestMessage
import json

config = None

def process_request(self, sqs_message):
    global config
    # extract/parse input JSON
    msg_body = sqs_message.body
    client_id = sqs_message.get_id()
    server_request_message = ServerRequestMessage(msg_body)

    # pull input file via S3
    input_bucket_handler = S3Handler(config.get_input_bucket_name())
    output_bucket_handler = S3Handler(config.get_output_bucket_name())

    # process file

    # create response output

    # upload response to output bucket under client_id_output_file_timestamp key

    # send message to response queue using client_id as  msg-id


def main():

    # load config
    config = Config("config.json")
    config.print_config()

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
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
from Config import Config

config = None

def process_request(self, sqs_message):
    global config
    sqs_request_handle = SQSHandler(config.get_response_queue_name(), 5)
    # extract/parse input JSON

    # pull input file via S3

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
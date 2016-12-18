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
import boto3

from SQSHandler import SQSHandler
from SQSHandler import SQSMessage

QUEUE_NAME = "snovak-queue-69-42-9001-1337-1984-20"
INPUT_FILE = "input2.txt"

def send_messages():
    input_file = open(INPUT_FILE, "r")
    lines = input_file.readlines()
    input_file.close()
    total_lines = len(lines)
    # have to be stated explicitly or else won't be fetched from AWS cloud
    sqs_handle = SQSHandler(QUEUE_NAME, total_lines)

    for i, line in enumerate(lines):
        msg = SQSMessage(line)
        msg.set_id(i)
        # indication for receiving end that each msg includes the inbox size
        # if this number is not specified, receiver can process messages as it sees fit
        msg.set_total_number(total_lines)
        print("Sending message: " + str(i+1) + "/" + str(total_lines))
        sqs_handle.send_message(msg)

def receive_messages():
    # ID is implicitly  set as msg attribute by SQS Handler


    # size can be determined from first received msg that includes total-msg-count attribute
    sqs_handle = SQSHandler(QUEUE_NAME)

    # since we know the total number of messages, we can block until all of them are received
    while not sqs_handle.is_inbox_full():
        sqs_handle.receive_messages()

    sqs_messages = sqs_handle.get_inbox().get_messages()

    output_file = open("output.txt", "w")
    for i, sqs_message in enumerate(sqs_messages):
        msg_content = sqs_message.get_message_body()
        print(sqs_message.get_message_body())
        output_file.write(str(msg_content))

    output_file.close()
    print("deleting queue")
    sqs_handle.delete()


def main():

    # each message should have a unique ID
    # each message should include the total number of messages
    # consumer maps each ID, and checks if all IDs were received

    send_messages()
    receive_messages()
    pass
    

if __name__ == '__main__':
    main()
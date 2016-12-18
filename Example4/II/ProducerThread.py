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

class ProducerThread (threading.Thread):
    def __init__(self, input_file_name, queue_name):
        threading.Thread.__init__(self)
        self.input_file_name = input_file_name
        self.queue_name = queue_name
    def run(self):
        print("\nStarting thread producer")

        input_file = open(self.input_file_name, "r")
        lines = input_file.readlines()
        input_file.close()
        total_lines = len(lines)
        # have to be stated explicitly or else won't be fetched from AWS cloud
        sqs_handle = SQSHandler(self.queue_name, total_lines)

        for i, line in enumerate(lines):
            msg = SQSMessage(line)
            msg.set_id(i)
            # indication for receiving end that each msg includes the inbox size
            # if this number is not specified, receiver can process messages as it sees fit
            msg.set_total_number(total_lines)
            print("PRODUCER_THREAD::::Sending message: " + str(i + 1) + "/" + str(total_lines))
            sqs_handle.send_message(msg)



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

class ConsumerThread (threading.Thread):
    def __init__(self, queue_name):
        threading.Thread.__init__(self)
        self.queue_name = queue_name

    def run(self):
        print ("Starting thread consumer")
        # size can be determined from first received msg that includes total-msg-count attribute
        sqs_handle = SQSHandler(self.queue_name)

        # since we know the total number of messages, we can block until all of them are received
        while not sqs_handle.is_inbox_full():
            print("CONSUMER_THREAD:::: receiving NEXT BATCH OF MSGS:: INBOX MSG COUNT:" + str(len(sqs_handle.get_inbox().get_messages())))
            sqs_handle.receive_messages()

        sqs_messages = sqs_handle.get_inbox().get_messages()

        output_file = open("output.txt", "w")
        for i, sqs_message in enumerate(sqs_messages):
            msg_content = sqs_message.get_message_body()
            print("CONSUMER_THREAD::::" + sqs_message.get_message_body())
            output_file.write(str(msg_content))

        output_file.close()
        print("deleting queue")
        sqs_handle.delete()

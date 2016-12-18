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



from ConsumerThread import ConsumerThread
from ProducerThread import ProducerThread

QUEUE_NAME = "snovak-queue-69-42-9001-1337-1984-14"
INPUT_FILE = "input.txt"

def main():

    # each message should have a unique ID
    # each message should include the total number of messages
    # consumer maps each ID, and checks if all IDs were received
    producer = ProducerThread(INPUT_FILE, QUEUE_NAME)
    consumer = ConsumerThread(QUEUE_NAME)

    producer.start()
    consumer.start()
    # join on consumer, end main as soon as all messages are received
    consumer.join()


if __name__ == '__main__':
    main()
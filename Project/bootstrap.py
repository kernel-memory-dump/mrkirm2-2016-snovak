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

from EC2Handler import EC2Handler
from Config import Config
from Config import *
from SQSHandler import SQSHandler
from S3Handler import S3Handler
from log import *

INIT_SCRIPT = "ec2_init_template.sh"


def main():

    handler = EC2Handler()
    config = acquire_config()

    print("Creating input/output buckets")

    s3_input_handle = S3Handler(config.get_input_bucket_name())
    s3_input_handle.create_new_public_bucket()
    s3_output_handle = S3Handler(config.get_output_bucket_name())
    s3_output_handle.create_new_public_bucket()

    print("Initializing request/response queues")
    write_to_log("Initializing request/response queues")
    sqs_request = SQSHandler(config.get_request_queue_name())
    sqs_response = SQSHandler(config.get_response_queue_name())

    print("Firing up EC2 server instance...")


    write_to_log("Initializing EC2 server...")
    handler.create_instance(INIT_SCRIPT)

    if handler.ec2_instance is None:
        print("Fatal error: failed to create EC2 instance!")
        return

    print("Initizalization completed! Server id is:" + handler.instance_id)
    print("Updating config.json, sending acquired server-id")
    config.set_server_id(handler.instance_id)
    config.update()


if __name__ == '__main__':
    main()
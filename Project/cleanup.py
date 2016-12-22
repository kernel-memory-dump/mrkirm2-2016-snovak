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



    config = acquire_config()

    print("Performing cleanup!!")

    print("Deleting buckets")
    s3_input_handle = S3Handler(config.get_input_bucket_name())
    s3_input_handle.delete_bucket()
    s3_output_handle = S3Handler(config.get_output_bucket_name())
    s3_output_handle.delete_bucket()

    print("Deleting request/response queues")
    write_to_log("Deleting request/response queues")
    sqs_request = SQSHandler(config.get_request_queue_name())
    sqs_response = SQSHandler(config.get_response_queue_name())

    sqs_request.delete()
    sqs_response.delete()

    print("Terminating EC2 server instance...")


    write_to_log("Terminating EC2 server...")
    handler = EC2Handler(None, config.get_server_id())
    handler.terminate_instance()

    config.set_server_id(-1)
    config.set_status("terminated")
    print("Cleanup completed! Server id now -1")
    print("Updating config.json, sending modified server-id")
    config.update()


if __name__ == '__main__':
    main()
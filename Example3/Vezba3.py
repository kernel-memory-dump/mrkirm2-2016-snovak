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
from S3Handler import S3Handler

# example for an existing bucket
SNOVAK_WORK_BUCKET = "snovak.propropr"


def main():

    # creating a new bucket with a randomly generated name
    s3Handler = S3Handler()
    s3Handler.create_new_bucket()

    # using an existing bucket
    #s3Handler = S3Handler(SNOVAK_WORK_BUCKET)

    s3Handler.upload_file('hello_world.py', 'hello_world.py')
    s3Handler.download_file('hello_world.py', 'hello_world_downloaded.py')
    s3Handler.delete_file('hello_world.py')
    s3Handler.delete_bucket()

if __name__ == '__main__':
    main()
    
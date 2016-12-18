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
import boto3

def get_random_prefix():
    """ Generates a new random bucket name with a prefix 'snovak.'

    Args:
        None
    Returns:
        (str) - newly generated bucket name

    """

    from time import time
    return "snovak." + str(time())
   

########## ERRORS #################################################
class S3HandlerError(Exception):
    """Wrapper for S3 resource error"""
    pass

class S3Handler(object):
    """Wrapper for S3 resource"""
    def __init__(self, bucket_name=None):
        self.s3_resource = boto3.resource('s3')
        self.bucket_name = bucket_name
        self.bucket = None
        if bucket_name is not None:
            self.bucket = self.s3_resource.Bucket(bucket_name)

    def create_new_public_bucket(self):
        """
        "Statement": [{
            "Sid": "AllowPublicRead",
            "Effect": "Allow",
            "Principal": {"AWS": "*"},
            "Action": ["s3:GetObject"],
            "Resource": ["arn:aws:s3:::bucket/*"]
        }
        """
        pass

    def create_new_bucket(self):
        # acquire a new bucket name if no bucket name was specified
        if self.bucket_name is None:
            self.bucket_name = get_random_prefix()
        self.bucket = self.s3_resource.create_bucket(Bucket=self.bucket_name)

    def upload_file(self, src, s3_key):
        """Attempts to upload specified file to current bucket

        Args:
            src (str): path to source file to be uploaded
            s3_key (str): value to be used as key in destination bucket
        Returns:
            None
        Raises:
            S3HandlerError if field 'bucket' is not initialized
        """
        self.bucket.upload_file(src, s3_key)

    def download_file(self, s3_key, dst):
        """Attempts to download specified file using s3_key and save it as 'dst'

        Args:
            s3_key (str): key to be used to locate file in bucket and download it
            dst (str): absolute file path where the downloaded file's content will be saved
        Returns:
            None
        Raises:
            S3HandlerError if field 'bucket' is not initialized
        """
        self.bucket.download_file(s3_key, dst)

    def delete_file(self, s3_key):
        """Attempts to delete specified file using s3_key

        Args:
            s3_key (str): key to be used to locate file in bucket and delete it
        Returns:
            None
        Raises:
            S3HandlerError if field 'bucket' is not initialized
        """
        self.bucket.delete_objects(Delete={'Objects': [{'Key': s3_key}]})
    
    def delete_bucket(self):
        self.bucket.delete()

    def get_bucket_name(self):
        return self.bucket_name

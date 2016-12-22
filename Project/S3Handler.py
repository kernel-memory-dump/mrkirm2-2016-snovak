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

def get_random_prefix(is_public=False):
    """ Generates a new random bucket name with a prefix 'snovak.'

    Args:
        None
    Returns:
        (str) - newly generated bucket name

    """

    from time import time
    if is_public:
        return "public.snovak.2016." + str(time())
    else:
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
        # acquire a new bucket name if no bucket name was specified
        if self.bucket_name is None:
            self.bucket_name = get_random_prefix(is_public=True)
        self.bucket = self.s3_resource.create_bucket(Bucket=self.bucket_name, ACL='public-read')

    def create_new_bucket(self):
        # acquire a new bucket name if no bucket name was specified
        if self.bucket_name is None:
            self.bucket_name = get_random_prefix()
        self.bucket = self.s3_resource.create_bucket(Bucket=self.bucket_name)

    def upload_file(self, src, s3_key, public=False):
        """Attempts to upload specified file to current bucket

        Args:
            src (str): path to source file to be uploaded
            s3_key (str): value to be used as key in destination bucket
            public (bool): if true, file will be made available to public, false by default
        Returns:
            None
        Raises:
            S3HandlerError if field 'bucket' is not initialized
        """
        self.bucket.upload_file(src, s3_key)
        if public:
            # apply ACL , grant read public for everyone
            self.bucket.upload_file(src, s3_key, ExtraArgs = {'ACL': 'public-read'})
        else:
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

    def is_bucket_created(self):
        from dateutil.parser import parse
        try:
            parse(self.bucket.creation_date)
            return True
        except:
            return False

    def delete_bucket(self):
        # empty whole bucket
        if not self.is_bucket_created():
            print("Empty bucket, nothing to delete")
            return
        for bucket_object in self.bucket.objects.all():
            print("Deleting object:" + str(bucket_object.key))
            bucket_object.delete()
        self.bucket.delete()

    def get_bucket_name(self):
        return self.bucket_name



if __name__ == '__main__':
    # test public bucket / public file
    """
    EXISTING_BUCKET_NAME = "snovak.public.input.bucket.2016.1234567890xxxxxyyyzzz2"
    s3_input_handle =  S3Handler(EXISTING_BUCKET_NAME)
    s3_input_handle.create_new_public_bucket()
    s3_input_handle.upload_file('test-file.txt', 'my-awesome-key', True)
    """

    s3_test_handle = S3Handler('snovak.public.input.bucket.2016.1234567890')
    s3_test_handle.download_file('snovak.client.1482355937.7394884__test-file.txt', 'slasdasdasdasd.json')


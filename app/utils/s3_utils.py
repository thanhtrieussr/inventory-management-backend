# s3_utils.py
import boto3
from botocore.exceptions import NoCredentialsError

s3 = boto3.client('s3', aws_access_key_id='YOUR_ACCESS_KEY', aws_secret_access_key='YOUR_SECRET_KEY')


def upload_to_s3(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name
    try:
        s3.upload_file(file_name, bucket, object_name)
        return True
    except FileNotFoundError:
        return False
    except NoCredentialsError:
        return False

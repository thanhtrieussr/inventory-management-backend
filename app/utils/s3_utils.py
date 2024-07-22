# app/utils/s3_utils.py
# Author: Thanh Trieu
# Description: Provides utilities for interacting with AWS S3, including file upload and URL generation.

import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from fastapi import HTTPException, UploadFile
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the S3 client
s3 = boto3.client('s3')

def get_bucket_name() -> str:
    """Retrieve the S3 bucket name from environment variables."""
    BUCKET_NAME = os.getenv('BUCKET_NAME')
    if not BUCKET_NAME:
        raise ValueError("BUCKET_NAME is not set in the environment variables")
    return BUCKET_NAME

def upload_file_to_s3(file: UploadFile, filename: str) -> str:
    """Upload a file to S3 and return the file URL."""
    BUCKET_NAME = get_bucket_name()
    try:
        s3.upload_fileobj(file.file, BUCKET_NAME, filename)
        file.file.close()  # Ensure the file is closed after upload
        return f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available")
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {e.response['Error']['Message']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

def generate_presigned_url(filename: str) -> str:
    """Generate a presigned URL to access a file in S3."""
    BUCKET_NAME = get_bucket_name()
    try:
        url = s3.generate_presigned_url('get_object',
                                        Params={'Bucket': BUCKET_NAME, 'Key': filename},
                                        ExpiresIn=3600)
        return url
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available")
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"URL generation failed: {e.response['Error']['Message']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"URL generation failed: {str(e)}")

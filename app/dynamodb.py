# dynamodb.py
import os
import time

import boto3
from dotenv import load_dotenv
import decimal


load_dotenv()  # Load environment variables from a .env file if present

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='us-east-1'  # Set your preferred region
)

table = dynamodb.Table(DYNAMODB_TABLE_NAME)


def log_api_call(endpoint, status_code, execution_time):
    table.put_item(
        Item={
            'endpoint': endpoint,
            'status_code': status_code,
            'execution_time': decimal.Decimal(str(execution_time)),  # Convert to string first
            'timestamp': int(time.time())
        }
    )

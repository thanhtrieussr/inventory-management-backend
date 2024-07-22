# app/dynamodb.py
# Author: Thanh Trieu
# Description: Contains functions for interacting with DynamoDB, including logging API calls.

import os
import time
import boto3
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Fetch AWS credentials and DynamoDB table name from environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")

# Initialize DynamoDB resource
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='us-east-1'  # Set your preferred region
)

# Reference to the DynamoDB table
table = dynamodb.Table(DYNAMODB_TABLE_NAME)

def log_api_call(endpoint: str, status_code: int, execution_time: float):
    """Log API call details to DynamoDB."""
    table.put_item(
        Item={
            'endpoint': endpoint,
            'status_code': str(status_code),  # Convert status_code to string
            'execution_time': str(execution_time),  # Convert execution_time to string
            'timestamp': str(int(time.time()))  # Convert timestamp to string
        }
    )

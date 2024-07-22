# tests/test_dynamodb.py
# Author: Thanh Trieu
# Description: Contains tests for logging API calls to DynamoDB.

import datetime
import os
import time
import unittest
from decimal import Decimal
import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='us-east-1'
)

table = dynamodb.Table(DYNAMODB_TABLE_NAME)

def log_api_call(endpoint, status_code, execution_time):
    timestamp = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    try:
        response = table.put_item(
            Item={
                'endpoint': endpoint,
                'status_code': status_code,
                'execution_time': str(execution_time),
                'timestamp': timestamp
            }
        )
        return str(execution_time)
    except Exception as e:
        print(f"Failed to log API call to DynamoDB: {e}")
        return None

class TestLogApiCall(unittest.TestCase):

    def test_log_api_call(self):
        endpoint = "/test-endpoint"
        status_code = 200
        execution_time = Decimal('0.123')

        logged_execution_time = log_api_call(endpoint, status_code, execution_time)

        self.assertIsNotNone(logged_execution_time, "Failed to log the API call.")

        time.sleep(1)

        response = table.get_item(
            Key={
                'endpoint': endpoint,
                'execution_time': logged_execution_time
            }
        )

        item = response.get('Item')
        self.assertIsNotNone(item, "Test failed. Item not found in DynamoDB.")
        if item:
            print("Test passed. Item found in DynamoDB.")
            print(item)

if __name__ == "__main__":
    unittest.main()

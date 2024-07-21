import datetime
import os
import time
import unittest
from decimal import Decimal
from dotenv import load_dotenv
import boto3

# Load environment variables from a .env file if present
load_dotenv()

# Define constants from environment variables
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

# Get the table
table = dynamodb.Table(DYNAMODB_TABLE_NAME)


# Define the log_api_call function
def log_api_call(endpoint, status_code, execution_time):
    print(f"Logging API Call - Endpoint: {endpoint}, Status: {status_code}, Execution Time: {execution_time}")
    try:
        timestamp = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
        response = table.put_item(
            Item={
                'endpoint': endpoint,
                'status_code': status_code,
                'execution_time': str(execution_time),  # Convert to string first
                'timestamp': timestamp
            }
        )
        print(f"DynamoDB Response: {response}")
        return str(execution_time)  # Return the exact execution_time used
    except Exception as e:
        print(f"Failed to log API call to DynamoDB: {e}")
        return None


# Define the test case class
class TestLogApiCall(unittest.TestCase):

    def test_log_api_call(self):
        endpoint = "/test-endpoint"
        status_code = 200
        execution_time = Decimal('0.123')

        # Log the API call and get the exact execution_time used
        logged_execution_time = log_api_call(endpoint, status_code, execution_time)

        # Ensure the log was successful
        self.assertIsNotNone(logged_execution_time, "Failed to log the API call.")

        # Allow some time for the log to be written to DynamoDB
        time.sleep(1)

        # Fetch the item from DynamoDB to verify
        response = table.get_item(
            Key={
                'endpoint': endpoint,
                'execution_time': logged_execution_time
            }
        )

        # Check if the item exists
        item = response.get('Item')
        self.assertIsNotNone(item, "Test failed. Item not found in DynamoDB.")
        if item:
            print("Test passed. Item found in DynamoDB.")
            print(item)


# Run the test
if __name__ == "__main__":
    unittest.main()

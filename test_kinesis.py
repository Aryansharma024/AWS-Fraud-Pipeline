import boto3
import json

kinesis_client = boto3.client('kinesis', region_name='ap-south-1')

transaction_data = {
    "UserID": "u123",
    "Amount": 45.50,
    "Location": "Tokyo"
}

print("Sending data to Kinesis...")
response = kinesis_client.put_record(
    StreamName='TransactionStream',
    Data=json.dumps(transaction_data),
    PartitionKey='u123' 
)

print("Success! AWS responded with:")
print(response)
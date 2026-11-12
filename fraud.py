import boto3
import json

kinesis_client = boto3.client('kinesis', region_name='ap-south-1')

fraudulent_transaction = {
    "UserID": "u123",
    "Amount": 500.00,
    "Location": "charampa"
}

response = kinesis_client.put_record(
    StreamName='TransactionStream',
    Data=json.dumps(fraudulent_transaction),
    PartitionKey='u123'
)
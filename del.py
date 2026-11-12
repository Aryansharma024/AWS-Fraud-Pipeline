import boto3
kinesis = boto3.client('kinesis', region_name='ap-south-1')
kinesis.delete_stream(StreamName='TransactionStream')
print("Stream deleted! You are no longer being charged.")
import boto3

dynamodb = boto3.client('dynamodb', region_name='ap-south-1')

print("Creating UserProfiles table...")
response = dynamodb.create_table(
    TableName='UserProfiles',
    KeySchema=[
        {
            'AttributeName': 'UserID',
            'KeyType': 'HASH'  
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'UserID',
            'AttributeType': 'S' 
        }
    ],
    BillingMode='PAY_PER_REQUEST' 
)

print("Waiting for AWS to build the table (this takes about 10-20 seconds)...")
waiter = dynamodb.get_waiter('table_exists')
waiter.wait(TableName='UserProfiles')

print("Success! Table is Active.")
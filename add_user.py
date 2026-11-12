import boto3

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('UserProfiles')

print("Adding baseline data for User u123...")
table.put_item(
    Item={
        'UserID': 'u123',
        'HomeLocation': 'New York',
        'DailyLimit': 500
    }
)
print("Success! User profile added to DynamoDB.")
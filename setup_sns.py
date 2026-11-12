import boto3

sns_client = boto3.client('sns', region_name='ap-south-1')

print("Creating FraudAlerts SNS Topic...")
topic_response = sns_client.create_topic(Name='FraudAlerts')
topic_arn = topic_response['TopicArn']

print(f"Topic created! Save this ARN for later: {topic_arn}")

my_email = "chinmayashuvchin@gmail.com"
print(f"Subscribing {my_email} to the Topic...")
sns_client.subscribe(
    TopicArn=topic_arn,
    Protocol='email',
    Endpoint=my_email
)

print("Success! Subscription created.")
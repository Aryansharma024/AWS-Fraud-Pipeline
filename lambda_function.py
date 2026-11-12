import json
import base64
import boto3

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
sns_client = boto3.client('sns', region_name='ap-south-1')

TABLE_NAME = 'UserProfiles'
SNS_TOPIC_ARN = 'arn:aws:sns:ap-south-1:056456546:FraudAlerts'  

def lambda_handler(event, context):
    table = dynamodb.Table(TABLE_NAME)
    
    for record in event['Records']:
        payload_bytes = base64.b64decode(record['kinesis']['data'])
        transaction = json.loads(payload_bytes.decode('utf-8'))
        
        user_id = transaction['UserID']
        tx_amount = float(transaction['Amount'])
        tx_location = transaction['Location']
        
        response = table.get_item(Key={'UserID': user_id})
        if 'Item' not in response:
            continue
            
        profile = response['Item']
        home_location = profile.get('HomeLocation')
        daily_limit = float(profile.get('DailyLimit', 0))
        
        is_fraud = False
        reasons = []
        
        if tx_amount > daily_limit:
            is_fraud = True
            reasons.append(f"Amount (${tx_amount}) exceeds daily limit (${daily_limit}).")
            
        if tx_location != home_location:
            is_fraud = True
            reasons.append(f"Location ({tx_location}) does not match home ({home_location}).")
            
        if is_fraud:
            alert_message = f"🚨 FRAUD ALERT 🚨\n\nUser: {user_id}\nTransaction: ${tx_amount} in {tx_location}\n\nReasons flagged:\n- " + "\n- ".join(reasons)
            
            sns_client.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="FRAUD DETECTED - Action Required",
                Message=alert_message
            )
            
    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete.')
    }
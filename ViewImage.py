import json
import boto3
import base64
import os
s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("*******", event)
    image_id = event['pathParameters']['imageid']
    s3_response = s3.get_object(Bucket=os.environ['bucket_name'], Key=image_id)
    image_data = base64.b64encode(s3_response['Body'].read()).decode('utf-8')
    
    return {
        'statusCode': 200,
        'body': json.dumps({'imageId': image_id, 'image': image_data})
    }

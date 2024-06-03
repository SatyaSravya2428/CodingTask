import json
import boto3
import base64
import uuid
import os
from datetime import date

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ["table_name"])

def lambda_handler(event, context):
    if 'content' not in event:
        return{
            'statusCode': 500,
            'message': 'Please upload a image file',
            'imageid' :''
            }

    image_data = base64.b64decode(event['content'])
    image_id = str(uuid.uuid4())
    
    s3.put_object(Bucket=os.environ["bucket_name"],
                    Key=image_id,
                    Body=image_data
                    )
    
    metadata = event['metadata'] if 'metadata' in event else {'type': 'image uploaded from testing'}
    item = {'imageid': image_id,
            'timestamp': str(date.today()),
            'metadata': metadata
    }
    try:
        table.put_item(Item=item)
        
        return {
            'statusCode': 200,
            'message': 'Successfully uploaded the image!',
            'imageid': image_id
        }
    except:
        return{
            'statusCode': 500,
            'message': 'Failed to update metdata in database',
            'imageid' :''
        }

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
    print(event)
    image_data = base64.b64decode(event['image'])
    image_id = str(uuid.uuid4())
    s3.put_object(Bucket=os.environ["bucket_name"],
                    Key=image_id,
                    Body=image_data
                    )
    
    metadata = event['metadata']
    item = {'imageid': image_id,
            'timestamp': str(date.today()),
            'metadata': metadata
    }
    table.put_item(Item=item)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'imageId': image_id})
    }
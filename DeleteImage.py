import json
import boto3
import os

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['table_name'])

def lambda_handler(event, context):
    image_id = event['pathParameters']['imageid']
    
    s3.delete_object(Bucket=os.environ['bucket_name'], Key=image_id)
    table.delete_item(Key={'imageId': image_id})
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Image deleted successfully'})
    }

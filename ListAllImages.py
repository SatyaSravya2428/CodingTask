import json
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['table_name'])

def lambda_handler(event, context):
    
    query_params = event.get('queryStringParameters', {})
    if not query_params :
        response = table.scan()
    else:
        imageid = query_params.get('imageid', None)
        timestamp = query_params.get('timestamp', None)
        
        print(imageid, timestamp)
        filter_expression = None
        if imageid:
            filter_expression = Attr('imageid').eq(imageid)
            if timestamp:
                filter_expression &= Attr('timestamp').eq(timestamp)
        if timestamp:
            filter_expression = Attr('timestamp').eq(timestamp)
    
    
        if filter_expression:
            response = table.scan(FilterExpression=filter_expression)
            if response is None:
                    return {
                   "isBase64Encoded": False,
                    "headers": { "Content-Type": "*/*"},
                    "statusCode": 500,
                    'body': 'No items found with the given imageid'
                }
    
    items = response['Items']
    
    return {
        "isBase64Encoded": False,
        "headers": { "Content-Type": "*/*"},
        "statusCode": 200,
        "body": json.dumps(items)
        }

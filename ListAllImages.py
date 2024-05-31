import json
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['table_name'])

def lambda_handler(event, context):
    
    print("*****", event)
    query_params = event.get('queryStringParameters', {})
    filter_key1 = query_params.get('filterKey1')
    filter_value1 = query_params.get('filterValue1')
    filter_key2 = query_params.get('filterKey2')
    filter_value2 = query_params.get('filterValue2')

    
    filter_expression = None
    if filter_key1 and filter_value1:
        filter_expression = Attr(filter_key1).eq(filter_value1)
    if filter_key2 and filter_value2:
        if filter_expression:
            filter_expression &= Attr(filter_key2).eq(filter_value2)
        else:
            filter_expression = Attr(filter_key2).eq(filter_value2)
    
    if filter_expression:
        response = table.scan(FilterExpression=filter_expression)
    else:
        response = table.scan()
    
    items = response['Items']
    
    return {
        'statusCode': 200,
        'body': json.dumps(items)
    }

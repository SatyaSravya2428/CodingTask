import json
import boto3
import os

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['table_name'])

def lambda_handler(event, context):
    image_id = event['pathParameters']['imageid']
    print("image", image_id, os.environ['bucket_name'])
    try:
        s3.delete_object(Bucket=os.environ['bucket_name'], Key=image_id)
    except s3.exceptions.NoSuchKey:
        return {
            'statusCode': 404,
            'body': json.dumps({'dmessage': 'File not found'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'dmessage': str(e)})
        }
    print("Bucket deletion is done!!! ")
    try:
        # check image from DynamoDB
        response = table.get_item(Key={'imageid': image_id})
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Image not found'})
            }
        # Delete the item if it exists
        table.delete_item(
            Key={'imageid': image_id},
            ConditionExpression="attribute_exists(imageid)"
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Image deleted successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }

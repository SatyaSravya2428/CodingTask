import json
import boto3
import base64
import os
s3 = boto3.client('s3')

def lambda_handler(event, context):
    image_id = event['pathParameters']['imageid']
    try:
        s3_response = s3.get_object(Bucket=os.environ['bucket_name'], Key=image_id)
    except s3.exceptions.NoSuchKey:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'File not found'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }
    image_data = base64.b64encode(s3_response['Body'].read()).decode('utf-8')
    
    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "application/jpg",
            "Content-Disposition": "attachment; filename- {}".format(image_id)
        },
        'isBase64Encoded': True,
        'body': image_data
    }

from flask import Flask, request, jsonify, send_file
import boto3
import os
from werkzeug.utils import secure_filename
from io import BytesIO
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# LocalStack S3 and DynamoDB configuration

localstack_url = "http://localhost:4566"
s3 = boto3.client('s3', endpoint_url=localstack_url, region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', endpoint_url=localstack_url, region_name='us-east-1')

# Create S3 bucket and DynamoDB table

bucket_name = "images-bucket"
table_name = "ImagesMetadata"

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Create S3 bucket
s3.create_bucket(Bucket=bucket_name)

# Create DynamoDB table
try:
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'image_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'image_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    table.wait_until_exists()
except Exception as e:
    table = dynamodb.Table(table_name)
    print("Exception while creting table", e)

# Helper function to generate unique image_id using uuid
def generate_image_id(filename):
    import uuid
    return f"{uuid.uuid4()}_{filename}"

#Upload image route
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file"}), 400

    image = request.files['image']
    metadata = {key: request.form[key] for key in request.form}
    image_id = generate_image_id(secure_filename(image.filename))

    s3.upload_fileobj(image, bucket_name, image_id)
    table.put_item(Item={'image_id': image_id, 'metadata': metadata})

    return jsonify({"image_id": image_id}), 200

#List images route
@app.route('/images', methods=['GET'])
def list_images():
    filter_key = request.args.get('filter_key')
    filter_value = request.args.get('filter_value')
    scan_kwargs = {}
    
    if filter_key and filter_value:
        scan_kwargs = {
            'FilterExpression': f"metadata.#k = :value",
            'ExpressionAttributeNames': {"#k": filter_key},
            'ExpressionAttributeValues': {":value": filter_value}
        }
    
    response = table.scan(**scan_kwargs)
    images = response.get('Items', [])
    return jsonify(images), 200

#Download image route
@app.route('/image/<image_id>', methods=['GET'])
def view_image(image_id):
    try:
        image_obj = s3.get_object(Bucket=bucket_name, Key=image_id)
        return send_file(BytesIO(image_obj['Body'].read()), mimetype='image/jpeg')
    except Exception as e:
        return jsonify({"error": str(e)}), 404

#Delete Image route
@app.route('/image/<image_id>', methods=['DELETE'])
def delete_image(image_id):
    try:
        s3.delete_object(Bucket=bucket_name, Key=image_id)
        table.delete_item(Key={'image_id': image_id})
        return jsonify({"message": "Image deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)

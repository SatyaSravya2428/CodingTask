import json
import requests
import base64

API_URL = " https://y2ctkccl06.execute-api.us-east-1.amazonaws.com/v1"
API_KEY = ""

headers = {
    "x-api-key": API_KEY,

}

def test_upload_image():
    url = f"{API_URL}/upload"
    image_path = '../Pictures/sample.png'
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    headers['Content-Type'] = "application/png"
    files = {
        'content': encoded_image
        }
    response = requests.post(url, files=files, headers=headers)
    assert response.status_code == 200
    assert "message" in response
    assert "imageid" in response
    data = response.json()
    return data['imageId']

def test_list_images():
    url = f"{API_URL}/allimages"
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "body" in data

def test_view_image(image_id):
    url = f"{API_URL}/viewimage/{image_id}"
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert 'body' in data

def test_delete_image(image_id):
    url = f"{API_URL}/deleteimage/{image_id}"
    response = requests.delete(url, headers=headers)
    assert response.status_code == 200

def run_tests():
    image_id = test_upload_image()
    test_list_images()
    test_view_image(image_id)
    test_delete_image(image_id)

if __name__ == "__main__":
    run_tests()

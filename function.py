import requests

def fetch_pictures(count):
    url = "https://place.dog/200/300"  # Image URL from place.dog
    images = []
    for _ in range(count):
        try:
            print(f"Requesting image from URL: {url}")
            response = requests.get(url, timeout=5)  # Adding timeout for reliability
            if response.status_code == 200:
                images.append(url)  # Append the URL directly
            else:
                print(f"Failed to fetch image: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching image: {e}")
    return images

# Test fetching 3 images
image_urls = fetch_pictures(3)
print(f"Fetched image URLs: {image_urls}")

import boto3
import uuid
import time

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')  # Replace with your AWS region
table = dynamodb.Table('AnimalPictures')  # Replace with your table name

def save_images_to_dynamodb(animal_type, image_urls):
    for image_url in image_urls:
        print(f"Saving image to DynamoDB: {image_url}")
        table.put_item(
            Item={
                'AnimalType': animal_type,
                'Timestamp': str(int(time.time() * 1000)),  # Current time in milliseconds
                'ImageURL': image_url,
                'ImageID': str(uuid.uuid4()),  # Unique identifier
            }
        )
    print("All images saved to DynamoDB!")

# Test saving 3 image URLs
animal_type = "dog"
image_urls = ["https://place.dog/200/300", "https://place.dog/200/300", "https://place.dog/200/300"]
save_images_to_dynamodb(animal_type, image_urls)


import boto3
from boto3.dynamodb.conditions import Key

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')  # Replace with your region
table = dynamodb.Table('AnimalPictures')  # Replace with your table name

def get_last_picture_timestamp(animal_type):
    try:
        # Query DynamoDB to get the latest picture
        response = table.query(
            KeyConditionExpression=Key('AnimalType').eq(animal_type),
            ScanIndexForward=False,  # Get the latest item
            Limit=1
        )

        if response.get('Items'):
            # Extract and return only the timestamp
            last_picture = response['Items'][0]
            return {"Timestamp": last_picture['Timestamp']}
        else:
            return {"error": f"No pictures found for {animal_type}"}
    except Exception as e:
        return {"error": str(e)}

# Test the function
if __name__ == "__main__":
    animal_type = "dog"  # Replace with the desired animal type
    result = get_last_picture_timestamp(animal_type)
    print(result)

import datetime

timestamp = 1735152102336
readable_timestamp = datetime.datetime.fromtimestamp(timestamp / 1000).isoformat()
print(readable_timestamp)

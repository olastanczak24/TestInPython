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

# Test fetching 1 image
image_url = fetch_pictures(1)
print(f"Fetched image URL: {image_url}")

import boto3
import uuid
import time

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')  # Replace with your AWS region
table = dynamodb.Table('AnimalPictures')  # Replace with your table name

def save_images_to_dynamodb(animal_type, image_url):
    for image_url in image_url:
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

# Test saving 1 image URL
animal_type = "dog"
image_url = ["https://place.dog/200/300"]
save_images_to_dynamodb(animal_type, image_url)

animal_type = "bear"
image_url = ["https://placebear.com/g/200/300"]
save_images_to_dynamodb(animal_type, image_url)


import boto3
from boto3.dynamodb.conditions import Key
import datetime

def get_last_saved_photo(animal_types):
    try:
        latest_photo = None
        latest_timestamp = None

        for animal_type in animal_types:
            # Query DynamoDB for the last saved photo of this animal type
            response = table.query(
                KeyConditionExpression=Key('AnimalType').eq(animal_type),
                ScanIndexForward=False,  # Get the most recent item
                Limit=1
            )

            if response.get('Items'):
                last_picture = response['Items'][0]
                raw_timestamp = last_picture.get('Timestamp')  # Safely retrieve the Timestamp field

                if not raw_timestamp:
                    print(f"Warning: Missing Timestamp for {animal_type}")
                    continue

                try:
                    raw_timestamp = int(raw_timestamp)  # Convert to integer
                except ValueError:
                    print(f"Warning: Invalid Timestamp format for {animal_type}")
                    continue

                readable_timestamp = datetime.datetime.fromtimestamp(raw_timestamp / 1000).isoformat()

                # Check if this is the latest across all animal types
                if latest_timestamp is None or raw_timestamp > latest_timestamp:
                    latest_photo = {
                        "AnimalType": animal_type,
                        "RawTimestamp": raw_timestamp,
                        "ReadableTimestamp": readable_timestamp,
                        "ImageURL": last_picture['ImageURL']
                    }
                    latest_timestamp = raw_timestamp

        if latest_photo:
            return latest_photo
        else:
            return {"error": "No valid photos found for the given animal types"}
    except Exception as e:
        return {"error": str(e)}

# Test the function
if __name__ == "__main__":
    # List of animal types to check
    animal_types = ["dog", "bear"]  # Add more if needed
    result = get_last_saved_photo(animal_types)

    if "error" not in result:
        print("Last saved photo details:")
        print(f"Animal Type: {result['AnimalType']}")
        print(f"Raw Timestamp: {result['RawTimestamp']}")
        print(f"Readable Timestamp: {result['ReadableTimestamp']}")
        print(f"Image URL: {result['ImageURL']}")
    else:
        print(result["error"])

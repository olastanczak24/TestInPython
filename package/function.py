import boto3
import requests
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('AnimalPictures')

API_URLS = {
    "dog": "https://place.dog/200/300"
}

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        animal_type = body.get('animalType')
        if animal_type not in API_URLS:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid animal type"})
            }

        response = requests.get(API_URLS[animal_type])
        if response.status_code != 200:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Failed to fetch image"})
            }

        
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }



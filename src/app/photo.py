from datetime import datetime
from .supabase_client import supabase
from dotenv import load_dotenv

import base64
import requests
import json
import os

def insert_photo():
    # Example test photo data
    data = {
        "url": "textURL.com",
        "creator": 827364,  # Use an actual user ID if you have auth set up
        "tags": [123, 234],  # Match your DB field type
        "date_created": str(datetime.utcnow().isoformat())
    }

    try:
        result = supabase.table("photo").insert(data).execute()
        print("Inserted photo:", result.data)
    except Exception as e:
        print("Failed to insert photo:", e)

if __name__ == "__main__":
    insert_photo()

def get_tags(image):
    # Reading the content of the image
    image_content = image.read()

    # Converting to base64
    base64_image = base64.b64encode(image_content).decode('utf-8')

    # Defining labels that the AI model can use for tags
    candidateLabels = ["cat", "dog", "car", "tree", "person", "beach", "forest"]

    # URL to call API
    url = "https://api-inference.huggingface.co/models/openai/clip-vit-base-patch32"

    # Body of the API call
    payload = json.dumps({
        "inputs": base64_image,
        "parameters": {
            "candidate_labels": candidateLabels
        }
    })

    # Loading .env file to get the API key
    load_dotenv()

    # Extracting the api key from the .env file
    api_key = os.getenv("HUGGING_FACE_API_KEY")

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {api_key}"
    }

    # Getting the response from the AI model
    response = requests.request("POST", url, headers=headers, data=payload)

    # Converting the response to a python dictionary
    json_response = response.json()

    # Initializing lists for the labels as well as the scores
    tags_list = []
    score_list = []

    for tag in json_response:
        tags_list.append(tag.get('label'))
        score_list.append(tag.get('score'))
    #print(f"labels: ", tags_list)
    #print(f"scores:", score_list)

    return tags_list, score_list
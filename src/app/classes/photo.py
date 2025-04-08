from app.supabase_client import supabase
from datetime import datetime
from dotenv import load_dotenv

import base64
import requests
import json
import os

class Photo:
    def __init__(self, url="no_url", creator="no_creator", tags=None):
        self.id = -1
        self.url = url
        self.creator = creator
        self.date_created = self.calculate_date()
        self.tags = tags if tags else [39909]
        if self.id == -1:
            self.get_id()

    def calculate_date(self):
        # Format: "MM-DD-YYYY"
        return datetime.now().strftime("%m-%d-%Y")

    def insert_into_database(self):
        data = {
            "url": self.url,
            "creator": self.creator,
            "date_created": self.date_created,
            "tags": self.tags
        }
        try:
            result = supabase.table("photo").insert(data).execute()
            print("Inserted photo:", result.data)
            self.id = self.get_id()
        except Exception as e:
            print("Failed to insert photo:", e)

    def get_id(self):
        try:
            result = supabase.table("photo").select("id").eq("url", self.url).execute()
            if result.data and len(result.data) > 0:
                self.id = result.data[0]["id"]
                return result.data[0]["id"]
        except Exception as e:
            print("Error fetching photo ID:", e)
        return -1

    def get_url(self):
        return self._fetch_field("url")

    def get_creator(self):
        return self._fetch_field("creator")

    def get_date_created(self):
        return self._fetch_field("date_created")

    def get_tags(self):
        return self._fetch_field("tags")

    def _fetch_field(self, field_name):
        if self.id == -1:
            print(f"photo.id not set, so photo.{field_name} cannot be fetched.")
            return None
        try:
            result = supabase.table("photo").select(field_name).eq("id", self.id).execute()
            if result.data and len(result.data) > 0:
                return result.data[0][field_name]
        except Exception as e:
            print(f"Error fetching photo.{field_name}:", e)
        return None

    def set_url(self, new_url):
        self._update_field("url", new_url)

    def set_creator(self, new_creator):
        self._update_field("creator", new_creator)

    def set_tags(self, new_tags):
        self._update_field("tags", new_tags)

    def _update_field(self, field_name, new_value):
        if self.id == -1:
            print(f"photo.id not set, so photo.{field_name} cannot be set.")
            return
        try:
            supabase.table("photo").update({field_name: new_value}).eq("id", self.id).execute()
            setattr(self, field_name, new_value)
        except Exception as e:
            print(f"Error updating photo.{field_name}:", e)

    def print_info(self):
        print("photo.id: ", self.get_id())
        print("photo.url: ", self.get_url())
        print("photo.creator: ", self.get_creator())
        print("photo.data_created: ", self.get_date_created())
        print("photo.tags: ", self.get_tags())

    def remove_from_database(self):
        if self.id == -1:
            print("photo.id not set, so this photo can't be deleted.")
            return
        try:
            supabase.table("photo").delete().eq("id", self.id).execute()
            print("Successfully deleted photo with id:", self.id)
        except Exception as e:
            print("Error deleting photo:", e)

    def generate_tags(self, image):
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

        # If the API does not work
        if response.status_code != 200:
            print(response)
            return

        # Converting the response to a python dictionary
        json_response = response.json()

        # Initializing lists for the labels as well as the scores
        tags_list = []
        score_list = []

        for tag in json_response:
            tags_list.append(tag.get('label'))
            score_list.append(tag.get('score'))

        return tags_list, score_list
    
    def generate_url(self, image):
        # URL for Imgur image upload
        url = "https://api.imgur.com/3/image"

        load_dotenv()

        imgur_api_key = os.getenv("IMGUR_API_KEY")

        # Setting up our authorization parameter
        headers = {
            'Authorization': 'Client-ID ' + imgur_api_key
        }

        try:
            # Setting up the files parameter for the API call
            files = [
                ('image', (image.name, image, image.content_type))
            ]

            # Make the POST request to upload the image
            response = requests.post(url, headers=headers, files=files)

            # Check the response status and print the result
            if response.status_code == 200:
                image_url = response.json()['data']['link']
                return image_url
            else:
                print("Failed to upload image. Response:", response.status_code, response.text)
                return
        except FileNotFoundError:
            print(f"Error: File not found.")
        except Exception as e:
            print(f"Error: {str(e)}")


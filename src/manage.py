#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import base64

# libraries for testing. Remove afterwords
from app.classes.user import *
from app.classes.tag import *
from app.classes.photo import *



def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    '''
    For some reason, the first time the AI model's API is requested, it fails.
    In order to fix this, we call the API with a sample image whenever the server starts.
    '''

    '''
    candidateLabels = ["cat", "dog", "car", "tree", "person", "beach", "forest"]

    image_path = os.path.join(os.path.dirname(__file__), 'app', 'static', 'ep233.png')

    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

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

    response = requests.request("POST", url, headers=headers, data=payload)
    print("Sent image to hugging face")
    print("Response; ", response.text)
    '''
    execute_from_command_line(sys.argv)

    


if __name__ == '__main__':
    main()

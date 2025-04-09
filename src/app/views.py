from django.shortcuts import render
from django.http import HttpResponse
from app.classes.photo import Photo
from app.classes.tag import Tag
from app.classes.user import User

import requests
import os

from app.globals import * # global constant variables

def index(request):
    context = {}
    if request.method == "POST":

        # If there is no file selected
        if not request.FILES.get("image"):
            return render(request, "app/index.html", {"error": "No file selected. Please upload an image."})
        
        # Getting all the images
        images = request.FILES.getlist('image')
        
        # Initializing context
        context = {
            "images_data": []
        }

        for image in images:
            # Creating an object of type photo
            im = Photo(image)

            # If the file type is incorrect
            if image.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
                return render(request, "app/index.html", {"error": "Incorrect file type. "
                "Please enter a .jpeg, .jpg, or .png image"})

            # Calling the generate_url function in the Photo class to get the imgur url
            image_url = im.generate_url(image)

            # If the image_url is not generated
            if not image_url:
                return render(request, "app/index.html", {"error": "URL not generated"})
            
            # Returning the pointer to the beginning of the photo
            image.seek(0)
            
            '''
            Note: I commented out the generation of tags in order to limit the amount of usage we have
            for the hugging face API. 
            
            If you need to test the API, you can uncomment the line:
                tags, scores = im.generate_tags(image)
            and comment out:
                tags = ' '
                scores = ' '
            '''
            tags, scores = im.generate_tags(image)
            #tags = 'Example'
            #scores = 'Example'

            if not tags and not scores:
                return render(request, "app/index.html", {"error": "AI model was unable to generate tags. Please try again."})

            # Adding name, url, tags, and scores to image_data
            image_data = {
                "name": image.name,
                "url": image_url,
                "tags_and_scores": zip(tags, scores)
            }

            # Initializing the tags array
            tag_ids = []
            # Inserting tags into the database
            # We only want to store the top 3 tags
            for tag in tags[:MAX_TAGS_PER_PHOTO]:
                t = Tag(tag)
                tag_ids.append(t.get_id())

            # Adding image data for each image to context
            context["images_data"].append(image_data)

            # Getting the creator's id
            c = User()
            creator = c.get_id()
            
            if creator is None:
                print("Creator not found, ")
                creator = "1dc54ee6-40ae-4d61-afb8-09958b911574"

            # Inserting tags into the database
            i = Photo(url=image_url, creator=creator, tags=tag_ids)
            i.insert_into_database()
        
    # If no errors, render upload_image.html
    return render(request, "app/index.html", context=context)

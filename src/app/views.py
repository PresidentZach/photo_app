from django.shortcuts import render
from django.http import HttpResponse
from app.classes.photo import Photo
from app.classes.tag import Tag


def index(request):
    return render(request, 'app/index.html')

def upload_image(request):
    if request.method == "POST":

        # If there is no file selected
        if not request.FILES.get("image"):
            return render(request, "app/upload_image.html", {"error": "No file selected. Please upload an image."})
        
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
                return render(request, "app/upload_image.html", {"error": "Incorrect file type. "
                "Please enter a .jpeg, .jpg, or .png image"})
            
            # Calling the generate tags function in Photo
            '''
            Note: I commented out the generation of tags in order to limit the amount of usage we have
            for the hugging face API. 
            
            If you need to test the API, you can uncomment the line:
                tags, scores = im.generate_tags(image)
            and comment out the two lines below.
            '''
            #tags, scores = im.generate_tags(image)
            tags = ' '
            scores = ' '

            # Calling the generate_url function in the Photo class to get the imgur url
            image_url = im.generate_url(image)

            # If the image_url is not generated
            if not image_url:
                return render(request, "app/upload_image.html", {"error": "URL not generated"})
            
            # Adding name, url, tags, and scores to image_data
            image_data = {
                "name": image.name,
                "url": image_url,
                "tags_and_scores": zip(tags, scores)
            }

            # Adding image data for each image to context
            context["images_data"].append(image_data)

        
    # If no errors, render upload_image.html
    return render(request, "app/upload_image.html", context=context)

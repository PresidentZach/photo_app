from django.shortcuts import render
from django.http import HttpResponse
from .photo import get_tags

def index(request):
    return render(request, 'app/index.html')

def upload_image(request):
    if request.method == "POST":
        # If there is no file selected
        if not request.FILES.get("image"):
            return render(request, "app/upload_image.html", {"error": "No file selected. Please upload an image."})
        
        # Getting the actual image
        image = request.FILES.get("image")

        # If the file type is incorrect
        if image.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
            return render(request, "app/upload_image.html", {"error": "Incorrect file type. "
            "Please enter a .jpeg, .jpg, or .png image"})
        tags, scores = get_tags(image)
        print(f"tags: ", tags)
        print(f"scores: ", scores)

        tags_and_scores = zip(tags, scores)

        context = {
            'tags': tags_and_scores
        }

        
    # If no errors, render upload_image.html
    return render(request, "app/upload_image.html", context=context)
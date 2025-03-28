from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'app/index.html')

def upload_image(request):
    if request.method == "POST" and request.FILES.get("image"):
        if not request.FILES.get("image"):
            return render(request, "app/upload_image.html", {"error": "No file selected. Please upload an image."})
    return render(request, "app/upload_image.html")
import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.classes.photo import Photo
from app.classes.tag import Tag
from app.classes.user import User
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


from app.globals import * # global constant variables

def index(request):

    context = {}

    # Getting the token of the user logged in
    token = request.session.get("supabase_token")

    # Creating a key in context for if a user is logged in
    context["logged_in"] = []
    # If they're logged in
    if token:
        # Filling in logged in key of context
        context["logged_in"].append("Logged in :)")

        # Fetch all photos of that user
        photo_object = User()

        photo_list = photo_object.fetch_photos(token=token)

        context["photo_list"] = photo_list
    
    if request.method == "POST":
        # If there is no file selected
        if not request.FILES.get("image"):
            context["error"] = "No file selected. Please upload an image."
            return render(request, "app/index.html", context=context)
        
        # Getting all the images
        images = request.FILES.getlist('image')
        
        # Initializing context
        context["images_data"] = []

        for image in images:
            # Creating an object of type photo
            im = Photo(image)

            # If the file type is incorrect
            if image.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
                context["error"] = "Incorrect file type. "
                "Please enter a .jpeg, .jpg, or .png image"

                return render(request, "app/index.html", context=context)

            # Calling the generate_url function in the Photo class to get the imgur url
            image_url = im.generate_url(image)

            # If the image_url is not generated
            if not image_url:
                context["error"] = "URL not generated."
                return render(request, "app/index.html", context=context)
            
            # Returning the pointer to the beginning of the photo
            image.seek(0)
            
            tags, scores = im.generate_tags(image)

            if tags == "None" and scores == "None":
                context["error"] = "AI model was unable to generate tags. Please try again."
                return render(request, "app/index.html", context=context)

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
            
            # Return error if we don't
            if creator is None:
                context["error"] = "CreatorID not found. Please log in."
                return render(request, "app/index.html", context=context)


            # Inserting tags into the database
            i = Photo(url=image_url, creator=creator, tags=tag_ids)
            i.insert_into_database()

    return render(request, "app/index.html", context=context)

"""
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User()
		
        try:
            token = user.login(email=email, password=password)
        except Exception as e:
            return render(request, "app/login.html", {"error": f"Error: {e}"})
        
        if token:
			# Store token in Django session
            request.session["supabase_token"] = token
            return redirect("index")
        else:
            return render(request, "app/login.html", {"error": "Invalid login."})
        
    return render(request, "app/login.html")
"""
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User()
        
        try:
            token = user.login(email=email, password=password)
        except Exception as e:
            # Pass the error message to the template
            return render(request, "app/login.html", {"error": "Email or password is incorrect."})
        
        if token:
            # Store token in Django session
            request.session["supabase_token"] = token
            return redirect("index")
        else:
            # Handle invalid login
            return render(request, "app/login.html", {"error": "Email or password is incorrect."})
        
    return render(request, "app/login.html")
    
def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User()

        signup_status = user.signup(email=email, password=password)

        if signup_status == "Already Exists":
            return render(request, "app/signup.html", {"message": "You already have an account. "
            "Please log in."})
        elif signup_status == "Needs Email":
            return render(request, "app/signup.html", {"message": "You have been sent a "
            "confirmation email. Please check your inbox."})
        else:
            # Catch other errors and show a generic error message
            return render(request, "app/signup.html", {"error": f"Error: {signup_status}"})
    
    return render(request, "app/signup.html")

def logout(request):
    user = User()

    # Signs out of supabase
    user.signout()

    # Clears the Django session
    request.session.flush()

    # Redirect to login
    return redirect("login")

def confirm_email(request):
    return render(request, "app/confirm.html", {
        "SUPABASE_URL": settings.SUPABASE_URL,
        "SUPABASE_ANON_KEY": settings.SUPABASE_ANON_KEY,
    })

def set_favorite(request):
    context = {}
    if request.method == "POST":
        id = request.POST.get("star")

    return render(request, "app/index.html")

    
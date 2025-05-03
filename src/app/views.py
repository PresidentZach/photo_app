from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.classes.photo import Photo
from app.classes.tag import Tag
from app.classes.user import User
from django.conf import settings

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

            if tags == "None" and scores == "None":
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
            
            # TODO: Make sure we actually get the creator ID
            # Return error if we don't
            if creator is None:
                print("Creator not found, ")

                # TODO: Return error here

                creator = "1dc54ee6-40ae-4d61-afb8-09958b911574"

            # Inserting tags into the database
            i = Photo(url=image_url, creator=creator, tags=tag_ids)
            i.insert_into_database()

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

        context["url_list"] = []
        # Loop through this list, for each item, return the url
        for photo in photo_list:
            context["url_list"].append(photo.get_url())

        return render(request, "app/index.html", context=context)

    return render(request, "app/index.html")


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

def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User()

        signup_status = user.signup(email=email, password=password)

        if signup_status == "Already Exists":
            return render(request, "app/login.html", {
                "message": f"You already have an account under {email}. Please log in."
            })
        elif signup_status == "Needs Email":
            return render(request, "app/login.html", {
                "message": f"You have been sent a confirmation email to {email}. "
                           "Please check your inbox. If you are struggling to find the email, "
                           "check your Spam / Junk folder."
            })
        else:
            # Catch other errors and show a generic error message
            return render(request, "app/login.html", {"error": f"Error: {signup_status}"})
    
    return render(request, "app/login.html")

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

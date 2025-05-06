import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from app.classes.photo import Photo
from app.classes.tag import Tag
from app.classes.user import User
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from app.globals import *  # global constant variables

def index(request):
    context = {}

    token = request.session.get("supabase_token")
    context["logged_in"] = []

    if token:
        context["logged_in"].append("Logged in :)")
        photo_object = User()
        photo_list = photo_object.fetch_photos(token=token)

        # Convert tag IDs to names
        for photo in photo_list:
            readable_tags = []
            for tag_id in photo.tags:
                t = Tag("placeholder", id=tag_id)
                tag_name = t.get_name()
                readable_tags.append(tag_name)

            photo.readable_tags = readable_tags

        context["photo_list"] = photo_list

    if request.method == "POST":
        if not request.FILES.get("image"):
            context["error"] = "No file selected. Please upload an image."
            return render(request, "app/index.html", context=context)

        images = request.FILES.getlist('image')
        context["images_data"] = []

        for image in images:
            im = Photo(image)

            if image.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
                context["error"] = "Incorrect file type. Please upload a .jpeg, .jpg, or .png image."
                return render(request, "app/index.html", context=context)

            image_url = im.generate_url(image)
            if not image_url:
                context["error"] = "URL not generated."
                return render(request, "app/index.html", context=context)

            image.seek(0)
            tags, scores = im.generate_tags(image)

            if tags == "None" and scores == "None":
                context["error"] = "AI model was unable to generate tags. Please try again."
                return render(request, "app/index.html", context=context)

            image_data = {
                "name": image.name,
                "url": image_url,
                "tags_and_scores": zip(tags, scores)
            }

            tag_ids = []

            for tag in tags[:MAX_TAGS_PER_PHOTO]:
                t = Tag(tag)
                tag_ids.append(t.get_id())

            context["images_data"].append(image_data)

            c = User()
            creator = c.get_id()

            if creator is None:
                context["error"] = "CreatorID not found. Please log in."
                return render(request, "app/index.html", context=context)

            i = Photo(url=image_url, creator=creator, tags=tag_ids)
            i.insert_into_database()

    return render(request, "app/index.html", context=context)

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User()

        try:
            token = user.login(email=email, password=password)
        except Exception:
            return render(request, "app/login.html", {"error": "Email or password is incorrect."})

        if token:
            request.session["supabase_token"] = token
            return redirect("index")
        else:
            return render(request, "app/login.html", {"error": "Email or password is incorrect."})

    return render(request, "app/login.html")

def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User()

        signup_status = user.signup(email=email, password=password)

        if signup_status in ["Already Exists", "Needs Email"]:
            return render(request, "app/signup.html", {"error": "An account already exists or a confirmation email has been sent."})
        else:
            return render(request, "app/signup.html", {"error": f"Error: {signup_status}"})

    return render(request, "app/signup.html")

def logout(request):
    user = User()
    user.signout()
    request.session.flush()
    return redirect("login")

def confirm_email(request):
    return render(request, "app/confirm.html", {
        "SUPABASE_URL": settings.SUPABASE_URL,
        "SUPABASE_ANON_KEY": settings.SUPABASE_ANON_KEY,
    })

@require_POST
@csrf_exempt
def delete_photo(request):
    try:
        # Parse JSON from request body
        body = json.loads(request.body)
        photo_id = body.get("photo_id")

        if not photo_id:
            return JsonResponse({"error": "Photo ID not provided."}, status=400)

        # Instantiate and assign ID
        photo = Photo()
        photo.id = int(photo_id)
        photo.remove_from_database()

        return JsonResponse({"success": True, "message": f"Photo {photo_id} deleted successfully."})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@require_POST
@csrf_exempt
def toggle_favorite(request):
    try:
        body = json.loads(request.body)
        photo_id = body.get("photo_id")

        if not photo_id:
            return JsonResponse({"error": "Photo ID not provided."}, status=400)

        photo = Photo()
        photo.id = int(photo_id)
        result = photo.set_is_favorited()  # Returns True if favorited, False if unfavorited

        return JsonResponse({
            "success": True,
            "favorited": result,
            "message": f"Photo {photo_id} is now {'favorited' if result else 'unfavorited'}."
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



"""
Not a class, but in the class folder because it functions like a class and may be implemented as one later. idk lol. 

The user needs to confirm their email address after signing up before logging in. 
We can turn this off if it complicates things. 

By default, when the user confirms their email address, they are redirected to
the SITE_URL. You can modify yourSITE_URL or add additional redirect URLs in your project.

TODO: Add error checking

"""

# global photo list for the user (list of photo objects)
global_user_photo_list = []
global_user_tags_to_select_from = ["cat", "dog", "car", "tree", "person", "beach", "forest"] # what tags are in it by default

from dotenv import load_dotenv
load_dotenv()

from app.supabase_client import supabase
from app.classes.photo import *

"""
NOTE: When a user signs up, they'll be sent an email where they have to verify their account. Until then, they 
cannot log in. Som the program should display a message when pressing the submit button to sign up that says something
like "Great! Next step is to verify your email. Please look out for an email in your inbox." Once they do that, within
supabase, we can actually redirect the email to the login page. 
"""

def user_signup(email="", password=""):
    response = supabase.auth.sign_up(
        { "email": email, "password": password, }
    )

def user_login(email="", password=""):
    response = supabase.auth.sign_in_with_password(
        { "email": email, "password": password, }
    )
    fetch_user_photos() # updates the global list of photos

def user_signout():
    response = supabase.auth.sign_out()
    global_user_photo_list = [] # clears the global list

def get_current_user_id():
    response = supabase.auth.get_user()
    if response and response.user:
        return response.user.id
    return None

def get_current_user_email():
    response = supabase.auth.get_user()
    if response and response.user:
        return response.user.email
    return None

def fetch_user_photos():
    user_id = get_current_user_id()
    if not user_id:
        print("No authenticated user found.")
        return []

    try:
        response = supabase.table("photo").select("*").eq("creator", user_id).execute()
        photos = response.data

        for photo_data in photos:
            photo = Photo(
                url=photo_data.get("url"),
                creator=photo_data.get("creator"),
                tags=photo_data.get("tags"),
            )
            photo.id = photo_data.get("id")
            photo.date_created = photo_data.get("date_created")
            global_user_photo_list.append(photo)

        return global_user_photo_list

    except Exception as e:
        print("Error fetching user photos:", e)
        return []

def get_user_photo_list():
    return global_user_photo_list
    # use this incase we decide to change how the global list is accessed. 

def get_user_tags_available():
    return global_user_tags_to_select_from

# function to print the ids of the photo objects for debug purposes. 
def print_photo_ids():
    temp_global_user_photo_list = get_user_photo_list()
    if not temp_global_user_photo_list:
        print("Photo list is empty.")
        return

    print("Photo IDs in the list:")
    for photo in temp_global_user_photo_list:
        print(photo.id)


"""
Not a class, but in the class folder because it functions like a class.

The user needs to confirm their email address after signing up before logging in. 
We can turn this off if it complicates things. 

By default, when the user confirms their email address, they are redirected to
the SITE_URL. You can modify yourSITE_URL or add additional redirect URLs in your project.

TODO: Add error checking

"""

from dotenv import load_dotenv
load_dotenv()

from app.supabase_client import supabase
from app.classes.photo import *

def user_signup(email="", password=""):
    response = supabase.auth.sign_up(
        { "email": email, "password": password, }
    )

def user_login(email="", password=""):
    response = supabase.auth.sign_in_with_password(
        { "email": email, "password": password, }
    )

def user_signout():
    response = supabase.auth.sign_out()

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
        user_photo_list = []

        for photo_data in photos:
            photo = Photo(
                url=photo_data.get("url"),
                creator=photo_data.get("creator"),
                tags=photo_data.get("tags"),
            )
            photo.id = photo_data.get("id")
            photo.date_created = photo_data.get("date_created")
            user_photo_list.append(photo)

        return user_photo_list

    except Exception as e:
        print("Error fetching user photos:", e)
        return []

# function to print the ids of the photo objects for debug purposes. 
def print_photo_ids(photo_list):
    if not photo_list:
        print("Photo list is empty.")
        return

    print("Photo IDs in the list:")
    for photo in photo_list:
        print(photo.id)

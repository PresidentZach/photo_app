

"""
The user needs to confirm their email address after signing up before logging in. 
We can turn this off if it complicates things. 

By default, when the user confirms their email address, they are redirected to
the SITE_URL. You can modify your SITE_URL or add additional redirect URLs in your project.

TODO: Add error checking

"""

from dotenv import load_dotenv
load_dotenv()

from app.globals import *
from app.supabase_client import supabase
from app.classes.photo import Photo

"""
NOTE: When a user signs up, they'll be sent an email where they have to verify their account. Until then, they 
cannot log in. Som the program should display a message when pressing the submit button to sign up that says something
like "Great! Next step is to verify your email. Please look out for an email in your inbox." Once they do that, within
supabase, we can actually redirect the email to the login page. 
"""

class User:
    def __init__(self):
        self.photo_list = []

    def signup(self, email="", password=""):
        # Try to log in first
        login_response = self.login(email=email, password=password)

        # If login is successful, the user already exists
        if login_response:  
            return "Already Exists"
        try:
            response = supabase.auth.sign_up(
                { "email": email, "password": password, }
            )
            
            user = response.user

            if user:
                # Check if email is confirmed or not
                if user.email_confirmed_at is None:
                    return "Needs Email"
            
            # If no user is returned, something went wrong
            return "Error: No user created. Please try again."
                    
        except KeyError as e:
            return f"KeyError: Missing expected key in response - {e}"
        except ConnectionError:
            return "Error: Unable to connect to the authentication server. Please check your network connection."
        except Exception as e:
            return f"Unexpected error: {str(e)}"

    def login(self, email="", password=""):
        try:
            response = supabase.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
            if response and response.user:
                self.fetch_photos(response.session.access_token)  # Fetch photos or other data after login
                return response.session.access_token  # Return the access token if login is successful
            return None
        except KeyError as e:
            return f"KeyError: Missing expected key in response - {e}"
        except ConnectionError:
            return "Error: Unable to connect to the authentication server. Please check your network connection."
        except Exception as e:
            return f"Unexpected error: {str(e)}"

    def signout(self):
        response = supabase.auth.sign_out()
        global_user_photo_list = [] # clears the global list
        if response: 
            return True
        return False

    def get_id(self):
        response = supabase.auth.get_user()
        if response and response.user:
            return response.user.id
        return None

    def get_email(self):
        response = supabase.auth.get_user()
        if response and response.user:
            return response.user.email
        return None

    # returns list of photo objects that belong to the user
    def fetch_photos(self, token):
        if not token:
            return []
        try:
            supabase.auth.set_session(token, token)
        except Exception as e:
            print(f"Authentication error: {e}")

        user_id = self.get_id()
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
                self.photo_list.append(photo)

            return self.photo_list

        except Exception as e:
            print("Error fetching user photos:", e)
            return []

    def get_photo_list(self):
        return self.global_user_photo_list
        # use this please incase we decide to change how the global list is accessed. 

    # function to print the ids of the photo objects for debug purposes. will be removed later
    def print_photo_ids(self):
        temp_global_user_photo_list = self.get_photo_list()
        if not temp_global_user_photo_list:
            print("Photo list is empty.")
            return

        print("Photo IDs in the list:")
        for photo in temp_global_user_photo_list:
            print(photo.id)
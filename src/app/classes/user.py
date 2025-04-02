

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

def get_current_user_display_name():
    True
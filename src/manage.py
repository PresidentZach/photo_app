#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# libraries for testing. Remove afterwords
from app.classes.user import *
from app.classes.tag import *
from app.classes.photo import *

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # user_login("zachstofko@proton.me", "Legorock12@")
    # print(get_current_user_id())
    # print(get_current_user_email())

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
    # create_new_user("zachstofko@proton.me", "Legorock12@")

    tag = Tag("test_tag_April3_2025_3")
    tag.insert_into_database()
    tag.get_id()
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from zip.models import Area, House, Review
from django.contrib.auth import get_user_model

import requests
from django.middleware.csrf import get_token
from django.test import RequestFactory

# Define the URL endpoint for creating a user
url = 'http://127.0.0.1:8000/usercontrol/user-config/'



# "key": "c6ea91baf8a41410ffa15519546a18e5fc86bcc8"
# Define the request payload

# Send the POST request


for i in range(4):
    data = {
    'email': f'test{i}@example.com',
    'id': f'test{i}',
    'nickname': f'test{i}',
    'password': 'theworld123',
    'age': 25,
    'sex': 'M',
    'major': 'Computer Science',
    'interested_areas' : [],
    }
    response = requests.post(url, json=data)

    print(response.json())

    
    
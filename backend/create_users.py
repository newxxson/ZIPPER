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

# Create a request object
request = RequestFactory().post('/')

# Get the CSRF token
csrf_token = get_token(request)

# Define the request headers
headers = {
    'X-CSRFToken': csrf_token,
}
# "key": "c6ea91baf8a41410ffa15519546a18e5fc86bcc8"
# Define the request payload
data = {
    'email': 'tututu@example.com',
    'id': 'tututu',
    'nickname': 'tututu',
    'password': 'theworld123',
    'age': 25,
    'sex': 'M',
    'major': 'Computer Science',
    'interested_areas': ['Anam-bub', 'Anam-bomun']
}

# Send the POST request
response = requests.post(url, headers=headers, json=data)

# Check the response status code
if response.status_code == 201:
    result = response.json()
    print(result)
else:
    print('Error creating user:', response)

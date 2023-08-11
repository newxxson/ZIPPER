import requests


def login():
    url = "http://ec2-13-125-213-208.ap-northeast-2.compute.amazonaws.com:8000/usercontrol/login/"  # Replace this with the actual URL of the server endpoint
    # url = 'http://127.0.0.1:8000/usercontrol/login/'
    # Define custom headers as a dictionary
    # headers = {
    #     'Authorization': 'Bearer YourAccessToken'
    # }
    data = {"username": "test0", "password": "theworld123"}

    response = requests.post(url, json=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = (
            response.json()
        )  # If the response contains JSON data, you can access it using the json() method
        print(data)
    else:
        print(f"Request failed with status code: {response}")


# login()


def area():
    url = "http://127.0.0.1:8000/api/areas"  # Replace this with the actual URL of the server endpoint
    key = "a9ab0d9ff961ee340d675a187ac5bea9f7f86342"

    # Define custom headers as a dictionary
    headers = {"Authorization": f"Token {key}"}

    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = (
            response.json()
        )  # If the response contains JSON data, you can access it using the json() method
        print(data)
    else:
        print(f"Request failed with status code: {response}")


# area()


def houses():
    url = "http://ec2-13-125-213-208.ap-northeast-2.compute.amazonaws.com:8000/api/houses/?simple"  # Replace this with the actual URL of the server endpoint
    # url = "http://127.0.0.1:8000/api/houses/?simple"  # Replace this with the actual URL of the server endpoint
    key = "a9ab0d9ff961ee340d675a187ac5bea9f7f86342"

    # Define custom headers as a dictionary
    headers = {"Authorization": f"Token {key}"}

    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = (
            response.json()
        )  # If the response contains JSON data, you can access it using the json() method
        print(data)
    else:
        # print(response.message)
        print(f"Request failed with status code: {response}")


houses()


def reviews():
    url = "http://ec2-13-125-213-208.ap-northeast-2.compute.amazonaws.com:8000/api/reviews/38/"  # Replace this with the actual URL of the server endpoint

    # url = 'http://127.0.0.1:8000/api/reviews/38'
    key = "989928d338332cc202c61a21abc60e976dedf828"

    # Define custom headers as a dictionary
    headers = {"Authorization": f"Token {key}"}

    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = (
            response.json()
        )  # If the response contains JSON data, you can access it using the json() method
        print(data)
    else:
        print(f"Request failed with status code: {response}")


# reviews()


def create_review_and_house():
    url = "http://127.0.0.1:8000/api/reviews/"
    key = "a9ab0d9ff961ee340d675a187ac5bea9f7f86342"

    # Define custom headers as a dictionary
    headers = {"Authorization": f"Token {key}"}
    data = {
        "area": "Anam-bub",
        "address": "서울시 동대문구 무학로 42길 35-1 (제기동)",
        "name": "안암빌라",
        "floor_type": "UP",
        "house_type": "OneRoom",
        "rent_type": "monthly",
        "deposit": 1000,
        "monthly": 60,
        "maintenance": 5,
        "keywords": [34, 35, 40, 45],
        "merits": "제발제발",
        "demerits": "plzplz",
        "rating_inside": 5,
        "rating_transport": 5,
        "rating_infra": 5,
        "rating_safety": 5,
        "rating_overall": 5,
        "suggest": 0,
    }

    response = requests.post(url, headers=headers, json=data)
    # Check if the request was successful (status code 200)
    if response.status_code == 201:
        data = (
            response.json()
        )  # If the response contains JSON data, you can access it using the json() method
        print(data)
    else:
        print(f"Request failed with status code: {response}")


# create_review_and_house()


def user_interest():
    url = "http://ec2-13-125-213-208.ap-northeast-2.compute.amazonaws.com:8000/api/user-interest/house/"  # Replace this with the actual URL of the server endpoint
    # url = "http://127.0.0.1:8000/api/user-interest/house"  # Replace this with the actual URL of the server endpoint
    key = "6ccbf57b7dedbdaedbdc66851401bc9cde206ee0"
    # Define custom headers as a dictionary
    headers = {"Authorization": f"Token {key}"}

    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = (
            response.json()
        )  # If the response contains JSON data, you can access it using the json() method
        print(data)
    else:
        print(f"Request failed with status code: {response}")


# user_interest()


def search_area():
    url = "http://127.0.0.1:8000/api/search/고려대로/?address"  # Replace this with the actual URL of the server endpoint
    key = "6ccbf57b7dedbdaedbdc66851401bc9cde206ee0"
    headers = {"Authorization": f"Token {key}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Request failed with status code: {response}")


# search_area()

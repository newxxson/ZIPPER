from backend.settings import NAVER_ID, NAVER_SECRET
import requests
import os
from datetime import datetime


def slice_and_get_coordinates(address):
    slice = address.find("(")
    if slice != -1:
        address = address[: (slice - 1)]

    # NCP 콘솔에서 복사한 클라이언트ID와 클라이언트Secret 값
    client_id = NAVER_ID
    client_secret = NAVER_SECRET

    # 주소 텍스

    endpoint = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    url = f"{endpoint}?query={address}"

    # 헤더
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
    }

    # 요청
    res = requests.get(url, headers=headers)
    result = res.json()
    data = result["addresses"][0]
    print(address, data["y"], data["x"])
    return (address, data["y"], data["x"])


def check_query(query_params, query_list):
    for query in query_params:
        condition = query_params.get(query)
        if query == "rent_type":
            if condition == "jeon":
                query_list["rent_type"] = condition
            elif condition == "monthly":
                query_list["rent_type"] = condition
        elif query == "dlb":
            query_list["deposit__gte"] = int(condition)
        elif query == "dub":
            query_list["deposit__lte"] = int(condition)
        elif query == "mlb":
            query_list["monthly__gte"] = int(condition)
        elif query == "mub":
            query_list["monthly__lte"] = int(condition)


def get_upload_to(instance, filename):
    username = instance.review.user.username
    house_name = instance.review.house.name

    time = datetime.now().strftime("%Y%m%d%H%M%S")

    extension = filename.split(".")[-1]
    new_filename = f"{house_name}_{username}_{time}.{extension}"

    return os.path.join("images", house_name, username, new_filename)


def calculate_suggest(house, suggest, method, original_suggest=None):
    if method == "delete":
        if suggest:
            house.suggest_ratio = (
                "%.2f"
                % ((house.suggest_ratio * house.review_num - 1))
                / (house.review_num - 1)
            )
        else:
            house.suggest_ratio = "%.2f" % (
                (house.suggest_ratio * house.review_num) / (house.review_num - 1)
            )
    elif method == "add":
        if suggest:
            print("suggesting")
            house.suggest_ratio = "%.2f" % (
                (house.review_num * house.suggest_ratio + 1) / (house.review_num + 1)
            )
        else:
            print("nosuggest")
            house.suggest_ratio = "%.2f" % (
                (house.review_num * house.suggest_ratio) / (house.review_num + 1)
            )
    elif method == "change":
        if original_suggest == 1 and suggest == 0:
            house.suggest_ratio = "%.2f" % (
                (house.suggest_ratio * house.review_num - 1) / house.review_num
            )
        elif original_suggest == 0 and suggest == 1:
            house.suggest_ratio = "%.2f" % (
                (house.suggest_ratio * house.review_num + 1) / house.review_num
            )

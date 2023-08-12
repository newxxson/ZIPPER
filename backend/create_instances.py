import os
import django
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from zip.models import Area, House, Review, Keyword
from django.contrib.auth import get_user_model

# def create_area_and_houses_and_reviews():
#     # Create Area instances
#     area1 = Area(area_code='Anam-bub', area_name='법후')
#     area1.save()

#     area2 = Area(area_code='Anam-bomun', area_name='보문')
#     area2.save()

#     # Create House instances for Area1
#     house1 = House(
#         address='123 Example Street, Anam-bub',
#         lat=123.456,  # lat value
#         lng=789.012,  # lng value
#         name='House 1 in 법후',
#         review_num=10,
#         interest_num=5,
#         suggest_ratio=0.6,
#         area=area1
#     )
#     house1.save()

#     house2 = House(
#         address='456 Example Avenue, Anam-bub',
#         lat=987.654,  # lat value
#         lng=210.987,  # lng value
#         name='House 2 in 법후',
#         review_num=15,
#         interest_num=8,
#         suggest_ratio=0.7,
#         area=area1
#     )
#     house2.save()

#     # Create House instances for Area2
#     house3 = House(
#         address='789 Example Road, Anam-bomun',
#         lat=654.321,  # lat value
#         lng=321.654,  # lng value
#         name='House 3 in 보문',
#         review_num=7,
#         interest_num=3,
#         suggest_ratio=0.4,
#         area=area2
#     )
#     house3.save()

#     house4 = House(
#         address='987 Example Lane, Anam-bomun',
#         lat=321.654,  # lat value
#         lng=654.321,  # lng value
#         name='House 4 in 보문',
#         review_num=12,
#         interest_num=6,
#         suggest_ratio=0.8,
#         area=area2
#     )
#     house4.save()

#     print("Area and House instances created successfully!")

#     UserModel = get_user_model()

#     user1 = UserModel.objects.get(id='liam')
#     user2 = UserModel.objects.get(id='tututu')

#     # Create Review instances for House 1
#     review1_house1 = Review(
#         user=user1,
#         house=house1,
#         floor_type='UP',
#         exit_year=2022,
#         house_type='apartment',
#         rent_type='monthly',
#         deposit=5000,
#         monthly=1000,
#         maintenance=200,
#         merits='Spacious rooms, great view',
#         demerits='Noisy neighbors, limited parking',
#         img_url='https://example.com/image1.jpg',
#         rating_inside=4.5,
#         rating_transport=3.8,
#         rating_infra=4.2,
#         rating_safety=4.0,
#         rating_overall=3.9,
#         suggest=True
#     )
#     review1_house1.save()

#     review2_house1 = Review(
#         user=user2,
#         house=house1,
#         floor_type='MID',
#         exit_year=2021,
#         house_type='House',
#         rent_type='monthly',
#         deposit=8000,
#         maintenance=300,
#         merits='Quiet neighborhood, spacious backyard',
#         demerits='Far from public transportation',
#         img_url='https://example.com/image2.jpg',
#         rating_inside=4.0,
#         rating_transport=2.5,
#         rating_infra=3.5,
#         rating_safety=4.2,
#         rating_overall=3.9,
#         suggest=False
#     )
#     review2_house1.save()

#     # Create Review instances for House 2
#     review1_house2 = Review(
#         user=user1,
#         house=house2,
#         floor_type='LOW',
#         exit_year=2023,
#         house_type='Condo',
#         rent_type='jeon',
#         deposit=3000,
#         monthly=800,
#         maintenance=150,
#         merits='Close to amenities, good security',
#         demerits='Limited parking space',
#         img_url='https://example.com/image3.jpg',
#         rating_inside=4.2,
#         rating_transport=4.5,
#         rating_infra=4.0,
#         rating_safety=4.0,
#         rating_overall=3.9,
#         suggest=True
#     )
#     review1_house2.save()

#     review2_house2 = Review(
#         user=user2,
#         house=house2,
#         floor_type='UP',
#         exit_year=2022,
#         house_type='Apartment',
#         rent_type='jeon',
#         deposit=4500,
#         monthly=1200,
#         maintenance=250,
#         merits='Modern design, great location',
#         demerits='Limited storage space',
#         img_url='https://example.com/image4.jpg',
#         rating_inside=4.8,
#         rating_transport=4.2,
#         rating_infra=4.5,
#         rating_safety=4.5,
#         rating_overall=3.9,
#         suggest=True
#     )
#     review2_house2.save()

#     review1_house3 = Review(
#         user=user1,
#         house=house3,
#         floor_type='UP',
#         exit_year=2022,
#         house_type='Apartment',
#         rent_type='monthly',
#         deposit=5000,
#         monthly=1000,
#         maintenance=200,
#         merits='Spacious rooms, great view',
#         demerits='Noisy neighbors, limited parking',
#         img_url='https://example.com/image1.jpg',
#         rating_inside=4.5,
#         rating_transport=3.8,
#         rating_infra=4.2,
#         rating_safety=4.0,
#         rating_overall=3.9,
#         suggest=True
#     )
#     review1_house3.save()

#     review2_house3 = Review(
#         user=user2,
#         house=house3,
#         floor_type='MID',
#         exit_year=2021,
#         house_type='House',
#         rent_type='jeon',
#         deposit=8000,
#         maintenance=300,
#         merits='Quiet neighborhood, spacious backyard',
#         demerits='Far from public transportation',
#         img_url='https://example.com/image2.jpg',
#         rating_inside=4.0,
#         rating_transport=2.5,
#         rating_infra=3.5,
#         rating_safety=4.2,
#         rating_overall=3.9,
#         suggest=False
#     )
#     review2_house3.save()

#     # Create Review instances for House 4
#     review1_house4 = Review(
#         user=user1,
#         house=house4,
#         floor_type='LOW',
#         exit_year=2023,
#         house_type='Condo',
#         rent_type='monthly',
#         deposit=3000,
#         monthly=800,
#         maintenance=150,
#         merits='Close to amenities, good security',
#         demerits='Limited parking space',
#         img_url='https://example.com/image3.jpg',
#         rating_inside=4.2,
#         rating_transport=4.5,
#         rating_infra=4.0,
#         rating_safety=4.0,
#         rating_overall=3.9,
#         suggest=True
#     )
#     review1_house4.save()

#     review2_house4 = Review(
#         user=user2,
#         house=house4,
#         floor_type='UP',
#         exit_year=2022,
#         house_type='Apartment',
#         rent_type='monthly',
#         deposit=4500,
#         monthly=1200,
#         maintenance=250,
#         merits='Modern design, great location',
#         demerits='Limited storage space',
#         img_url='https://example.com/image4.jpg',
#         rating_inside=4.8,
#         rating_transport=4.2,
#         rating_infra=4.5,
#         rating_safety=4.5,
#         rating_overall=3.9,
#         suggest=True
#     )
#     review2_house4.save()

#     print("Review instances created successfully!")


# create_area_and_houses_and_reviews()

# from zip.models import Keyword

# def create_keywords():
#     key_choices = [('INFRA', 'Infrastructure'), ('ROOM', 'Room Condition'), ("SAFETY", "Safety"), ('TRANSPORT', 'Transportation method')]

#     # Define four descriptions for each key_type
#     descriptions = {
#         'INFRA': ['Good infrastructure', 'Well-maintained facilities', 'Modern amenities', 'High-quality infrastructure'],
#         'ROOM': ['Beautifully designed rooms', 'Spacious living areas', 'Comfortable bedrooms', 'Well-furnished interiors'],
#         'SAFETY': ['Safe neighborhood', 'Secure environment', 'Good security measures', 'Peaceful and secure surroundings'],
#         'TRANSPORT': ['Convenient transportation options', 'Accessible to public transport', 'Close to major routes', 'Easy commute']
#     }

#     # Create Keyword instances
#     for key_type, _ in key_choices:
#         for index, description in enumerate(descriptions[key_type], 1):
#             icon_url = f'https://example.com/icon/{key_type}/{index}.png'
#             keyword = Keyword(key_type=key_type, description=description, icon_url=icon_url)
#             keyword.save()

#     print("Keyword instances created successfully!")


# # create_keywords()


def create_real_instances():
    reviews = [
        {
            "token": "b2841dcd8051a1f94c1e197edb47a4487a926347",
            "floor_type": "UP",
            "exit_year": 2022,
            "house_type": "OneRoom",
            "rent_type": "monthly",
            "deposit": 5000,
            "monthly": 1000,
            "maintenance": 200,
            "merits": "깨끗해서 좋은듯 더러워서 싫은듯 아냐 그냥 좋은듯 아니다 그냥 안좋은듯",
            "demerits": "이하동문이하동문이하동문이하동문이하동문이하동문이하동문",
            "rating_inside": 3,
            "rating_transport": 3,
            "rating_infra": 4,
            "rating_safety": 4,
            "rating_overall": 4,
            "suggest": False,
            "keywords": [1, 6, 11, 16],
            "address": "서울특별시 성북구 고려대로 89",
            "area": "Anam-Station",
        },
        {
            "token": "d249559ee2f5fee28bb977b03b476a51624b1ca7",
            "floor_type": "UP",
            "exit_year": 2022,
            "house_type": "OneRoom",
            "rent_type": "monthly",
            "deposit": 5000,
            "monthly": 1000,
            "maintenance": 200,
            "merits": "넓은 방, 멋진 전망",
            "demerits": "시끄러운 이웃, 주차 공간 한정",
            "rating_inside": 2,
            "rating_transport": 4,
            "rating_infra": 5,
            "rating_safety": 4,
            "rating_overall": 4,
            "suggest": True,
            "keywords": [1, 6, 11, 16],
            "address": "서울특별시 성북구 고려대로 89",
            "area": "Anam-Station",
        },
        {
            "token": "a9d08944c467bb903c93a1b96ef17ae8584fd19f",
            "floor_type": "UP",
            "exit_year": 2022,
            "house_type": "OneRoom",
            "rent_type": "monthly",
            "deposit": 5000,
            "monthly": 1000,
            "maintenance": 200,
            "merits": "넓은 방, 멋진 전망",
            "demerits": "시끄러운 이웃, 주차 공간 한정",
            "rating_inside": 5,
            "rating_transport": 5,
            "rating_infra": 5,
            "rating_safety": 3,
            "rating_overall": 5,
            "suggest": True,
            "keywords": [1, 6, 11, 16],
            "address": "서울특별시 성북구 고려대로 89",
            "area": "Anam-Station",
        },
        {
            "token": "55a20cf2ef6dbb9a1fc822f477b22ace3d642936",
            "floor_type": "UP",
            "exit_year": 2023,
            "house_type": "OneRoom",
            "rent_type": "monthly",
            "deposit": 4000,
            "monthly": 1200,
            "maintenance": 100,
            "merits": "조용한 동네, 정원 공간",
            "demerits": "대중교통 제한적, 작은 주방",
            "rating_inside": 4,
            "rating_transport": 3,
            "rating_infra": 3,
            "rating_safety": 5,
            "rating_overall": 4,
            "suggest": True,
            "keywords": [1, 6, 11, 16],
            "address": "서울 성북구 개운사길 19",
            "area": "Anam-Gaeun",
        },
        {
            "token": "b2841dcd8051a1f94c1e197edb47a4487a926347",
            "floor_type": "UP",
            "exit_year": 2023,
            "house_type": "OneRoom",
            "rent_type": "monthly",
            "deposit": 3500,
            "monthly": 1100,
            "maintenance": 150,
            "merits": "넓은 거실, 근처에 공원",
            "demerits": "길가 소음, 저장공간 부족",
            "rating_inside": 4,
            "rating_transport": 4,
            "rating_infra": 4,
            "rating_safety": 3,
            "rating_overall": 4,
            "suggest": True,
            "keywords": [1, 6, 11, 16],
            "address": "서울 성북구 개운사길 19",
            "area": "Anam-Gaeun",
        },
        {
            "token": "d249559ee2f5fee28bb977b03b476a51624b1ca7",
            "floor_type": "UP",
            "exit_year": 2023,
            "house_type": "OneRoom",
            "rent_type": "monthly",
            "deposit": 4000,
            "monthly": 1300,
            "maintenance": 100,
            "merits": "조용한 동네, 넓은 방",
            "demerits": "대중교통 제한적, 오래된 가전제품",
            "rating_inside": 3,
            "rating_transport": 3,
            "rating_infra": 4,
            "rating_safety": 4,
            "rating_overall": 3,
            "suggest": False,
            "keywords": [1, 6, 11, 16],
            "address": "서울특별시 동대문구 제기로2길 29",
            "area": "Anam-Front",
        },
        {
            "token": "a9d08944c467bb903c93a1b96ef17ae8584fd19f",
            "floor_type": "UP",
            "exit_year": 2023,
            "house_type": "OneRoom",
            "rent_type": "monthly",
            "deposit": 3000,
            "monthly": 800,
            "maintenance": 50,
            "merits": "편리한 위치, 저렴한 가격",
            "demerits": "공간이 제한적, 주차 불가능",
            "rating_inside": 3,
            "rating_transport": 4,
            "rating_infra": 3,
            "rating_safety": 3,
            "rating_overall": 3,
            "suggest": True,
            "keywords": [1, 6, 11, 16],
            "address": "서울특별시 동대문구 제기로2길 29",
            "area": "Anam-Front",
        },
        {
            "token": "55a20cf2ef6dbb9a1fc822f477b22ace3d642936",
            "floor_type": "UP",
            "exit_year": 2023,
            "house_type": "OneRoom",
            "rent_type": "monthly",
            "deposit": 3200,
            "monthly": 850,
            "maintenance": 60,
            "merits": "새로 리모델링한, 편의시설 가까운",
            "demerits": "자연광 제한적, 길 소음 있어요",
            "rating_inside": 4,
            "rating_transport": 4,
            "rating_infra": 4,
            "rating_safety": 3,
            "rating_overall": 4,
            "suggest": True,
            "keywords": [1, 6, 11, 16],
            "address": "서울특별시 동대문구 제기로2길 29",
            "area": "Anam-Front",
        },
        {
            "token": "b2841dcd8051a1f94c1e197edb47a4487a926347",
            "floor_type": "UP",
            "exit_year": 2023,
            "house_type": "OneRoom",
            "rent_type": "monthly",
            "deposit": 2800,
            "monthly": 750,
            "maintenance": 50,
            "merits": "조용한 지역, 애완동물 허용",
            "demerits": "시설 제한적, 발코니 없어요",
            "rating_inside": 3,
            "rating_transport": 3,
            "rating_infra": 3,
            "rating_safety": 4,
            "rating_overall": 3,
            "suggest": False,
            "keywords": [1, 6, 11, 16],
            "address": "서울특별시 동대문구 제기로2길 29",  # j
            "area": "Anam-Front",
        },
    ]
    url = "http://ec2-13-125-213-208.ap-northeast-2.compute.amazonaws.com:8000/api/reviews/"

    for i, review in enumerate(reviews):
        key = review.pop("token")
        headers = {"Authorization": f"Token {key}"}
        review["name"] = f"{review['area']} / 안암{i}"
        response = requests.post(url, headers=headers, json=review)

        if response.status_code == 201:
            data = response.json()
            print(i, data)
        else:
            print(f"Request failed with status code: {response}")
            print(response.json())
            print(i)
            break


# create_real_instances()


# def create_review_and_house():
#     url = "http://ec2-13-125-213-208.ap-northeast-2.compute.amazonaws.com:8000/api/reviews/"
#     key = "a9ab0d9ff961ee340d675a187ac5bea9f7f86342"

#     # Define custom headers as a dictionary
#     headers = {"Authorization": f"Token {key}"}
#     data = {
#         "area": "Anam-bub",
#         "address": "서울시 동대문구 제기동 148-26",
#         "lat": "12.0.0.4",
#         "lng": "13.0.0.15",
#         "name": "제발돼라",
#         "floor_type": "UP",
#         "house_type": "원룸",
#         "rent_type": "monthly",
#         "deposit": 1000,
#         "monthly": 60,
#         "maintenance": 5,
#         "keywords": [1, 6, 11, 16],
#         "merits": "제발제발",
#         "demerits": "plzplz",
#         "img_url": "https://urls.png",
#         "rating_inside": 5,
#         "rating_transport": 5,
#         "rating_infra": 5,
#         "rating_safety": 5,
#         "rating_overall": 5,
#         "suggest": 0,
#     }

#     response = requests.post(url, headers=headers, json=data)
#     # Check if the request was successful (status code 200)
#     if response.status_code == 201:
#         data = (
#             response.json()
#         )  # If the response contains JSON data, you can access it using the json() method
#         print(data)
#     else:
#         print(f"Request failed with status code: {response}")


# Make sure to import your Keyword model


def create_keywords():
    examples = [
        {
            "key_type": "INFRA",
            "description": "물 공급 좋음",
            "icon_url": "https://example.com/water-icon.png",
        },
        {
            "key_type": "INFRA",
            "description": "전기 사용 편함",
            "icon_url": "https://example.com/electricity-icon.png",
        },
        {
            "key_type": "INFRA",
            "description": "난방 시스템 좋음",
            "icon_url": "https://example.com/heating-icon.png",
        },
        {
            "key_type": "INFRA",
            "description": "공기 환기 잘됨",
            "icon_url": "https://example.com/ventilation-icon.png",
        },
        {
            "key_type": "ROOM",
            "description": "방 깨끗함",
            "icon_url": "https://example.com/cleanliness-icon.png",
        },
        {
            "key_type": "ROOM",
            "description": "가구 상태 좋음",
            "icon_url": "https://example.com/furniture-icon.png",
        },
        {
            "key_type": "ROOM",
            "description": "공간 활용 잘됨",
            "icon_url": "https://example.com/space-icon.png",
        },
        {
            "key_type": "ROOM",
            "description": "편의 시설 다양함",
            "icon_url": "https://example.com/amenities-icon.png",
        },
        {
            "key_type": "SAFETY",
            "description": "화재 안전 지킴",
            "icon_url": "https://example.com/fire-safety-icon.png",
        },
        {
            "key_type": "SAFETY",
            "description": "보안 철저함",
            "icon_url": "https://example.com/security-icon.png",
        },
        {
            "key_type": "SAFETY",
            "description": "비상 탈출로 있음",
            "icon_url": "https://example.com/exit-icon.png",
        },
        {
            "key_type": "SAFETY",
            "description": "CCTV 관찰 중",
            "icon_url": "https://example.com/cctv-icon.png",
        },
        {
            "key_type": "TRANSPORT",
            "description": "버스정류장 가까움",
            "icon_url": "https://example.com/public-transport-icon.png",
        },
        {
            "key_type": "TRANSPORT",
            "description": "주차 편리함",
            "icon_url": "https://example.com/parking-icon.png",
        },
        {
            "key_type": "TRANSPORT",
            "description": "접근성 좋음",
            "icon_url": "https://example.com/accessibility-icon.png",
        },
        {
            "key_type": "TRANSPORT",
            "description": "차량 렌탈 가능",
            "icon_url": "https://example.com/rental-icon.png",
        },
    ]
    for example in examples:
        Keyword.objects.create(
            key_type=example["key_type"],
            description=example["description"],
            icon_url=example["icon_url"],
        )


# Call the function to create the keywords
create_keywords()
create_real_instances()

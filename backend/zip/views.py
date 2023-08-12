from django.shortcuts import render
from .serializers import (
    HouseSerializer,
    HouseSerializerSimple,
    AreaSerializer,
    AreaSerializerSimple,
    KeywordSerializer,
    ReviewSerializer,
)
from rest_framework import viewsets
from .models import Area, House, Keyword, Review
from rest_framework.response import Response
from itertools import groupby
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsWriterOrAdmin, IsReadOnlyOrAdmin
from rest_framework.decorators import api_view, permission_classes
import json
from backend.settings import NAVER_ID, NAVER_SECRET
from .utils import slice_and_get_coordinates, check_query
from django.core.mail import EmailMessage, get_connection, send_mail
from django.conf import settings
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


# used to see houses related to each area, can specify area
class AreaView(viewsets.ModelViewSet):
    serializer_class = AreaSerializer
    queryset = Area.objects.all()
    permission_classes = [IsAuthenticated, IsReadOnlyOrAdmin]
    lookup_field = "area_code"

    def list(self, request, *args, **kwargs):
        query_params = request.query_params

        if not query_params:
            return super().list(request, *args, **kwargs)
        elif query_params.get("simple"):
            serializer = AreaSerializerSimple(instance=self.queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Invalid query parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# 1. retreive only coordinates and ratio
# 2. retreive all the house instance => pagination not supported yet
# 3. retreive specific house instance with address(postal_code)
# 4. retreive house matching to search parameter
class HouseView(viewsets.ModelViewSet):
    serializer_class = HouseSerializer
    lookup_field = "address"
    queryset = House.objects.all()
    permission_classes = [IsAuthenticated, IsReadOnlyOrAdmin]

    # simple list는 허용됨
    def get_permissions(self):
        if self.action == "list" and "simple" in self.request.query_params:
            return []
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        query_params = request.query_params
        instance = self.queryset
        if not query_params:
            print("no query")
            serializer = self.get_serializer(instance, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif "simple" in query_params:
            print("simple")
            serializer = self.get_serializer(instance, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise ValidationError("Invalid query parameter.")

    # 주소를 물으면 집들을 리턴, pk를 특정하면 리뷰를 리턴
    def retrieve(self, request, *args, **kwargs):
        data = self.kwargs.get(self.lookup_field)
        if data.isnumeric():
            house = self.queryset.get(pk=data)
            reviews = house.reviews.all()
            serializer = ReviewSerializer(
                reviews, many=True, context={"user": request.user}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            result = self.queryset.filter(address__contains=data)
            serializer = self.get_serializer(result, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == "list" and "simple" in self.request.query_params:
            return HouseSerializerSimple
        return self.serializer_class


# deprececated now search is used from multi search view but create is still used
class ReviewView(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated, IsWriterOrAdmin]

    def list(self, request, *args, **kwargs):
        query_params = request.query_params

        if not query_params:
            serializer = self.get_serializer(
                self.queryset, many=True, context={"user": request.user}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        query_list = dict()

        for query in query_params:
            self.check_query(query, query_params, query_list)
        print(query_list)
        result = self.queryset.filter(**query_list)
        serializer = self.get_serializer(
            result, many=True, context={"user": request.user}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        id = self.kwargs.get(self.lookup_field)
        review = Review.objects.get(id=id)
        serializer = self.get_serializer(review, context={"user": request.user})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 용어를 정리할 필요가 있음
    def check_query(self, query, query_params, query_list):
        condition = query_params.get(query)
        print(query, type(query), condition, type(condition))
        if query == "area":
            query_list["house__area__area_code"] = condition
        elif query == "rent":
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

    def create(self, request, *args, **kwargs):
        print(request.data)
        try:
            data_dict = request.data.get("json_data")
            data_dict = json.loads(data_dict)
        except:
            data_dict = request.data
            print(type(data_dict))

        address = data_dict.pop("address")
        address, lat, lng = slice_and_get_coordinates(address)
        house_queryset = House.objects.filter(address=address)
        try:
            if house_queryset.exists():
                house_instance = house_queryset.first()

                if house_instance.reviews.filter(user=request.user).exists():
                    return Response(
                        {"message": "the user has already written the Review"},
                        status=status.HTTP_409_CONFLICT,
                    )

                # house 정보 수정
                suggest_ratio = house_instance.suggest_ratio
                review_num = house_instance.review_num
                if data_dict.get("suggest") == 1:
                    print("suggesting")
                    house_instance.suggest_ratio = "%.2f" % (
                        (review_num * suggest_ratio + 1) / (review_num + 1)
                    )
                else:
                    print("nosuggest")
                    house_instance.suggest_ratio = "%.2f" % (
                        (review_num * suggest_ratio) / (review_num + 1)
                    )
                house_instance.review_num += 1
                house_instance.save()
            else:
                if data_dict.get("suggest") == 1:
                    suggest_ratio = 1
                else:
                    suggest_ratio = 0
                area = Area.objects.get(area_code=data_dict.get("area"))
                house_instance = House.objects.create(
                    area=area,
                    address=address,
                    lat=lat,
                    lng=lng,
                    name=data_dict.get("name"),
                    suggest_ratio=suggest_ratio,
                )
                print("house_created")

            # review 형식에 맞게 수정
            data_dict.pop("area")
            data_dict.pop("name")
            key_pk = data_dict.pop("keywords")
            print(key_pk)
            keywords = Keyword.objects.filter(pk__in=key_pk)

            img_url = ""
            try:
                image_data = request.FILES.get("image_data")
            except Exception as e:
                print(e)
                img_url = "https://test.com/testtest.png"

            review_instance = Review.objects.create(
                user=request.user, house=house_instance, img_url=img_url, **data_dict
            )
            review_instance.keywords.set(keywords)
            review_instance.save()
            print("review created")
            serializer = self.get_serializer(
                review_instance, context={"user": request.user}
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        house = instance.house
        data_dict = request.data

        suggest = data_dict.get("suggest")

        # 집 suggest_ratio 수정
        if suggest != None:
            if suggest == 1 and instance.suggest == 0:
                house.suggest_ratio = "%.2f" % (
                    (house.suggest_ratio * house.review_num + 1) / house.review_num
                )
            elif suggest == 0 and instance.suggest == 1:
                house.suggest_ratio = "%.2f" % (
                    (house.suggest_ratio * house.review_num - 1) / house.review_num
                )
            house.save()
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        house = instance.house
        if house.review_num == 1:
            print("destroy house")
            return super().destroy(request, *args, **kwargs)

        if instance.suggest:
            house.suggest_ratio = "%.2f" % (
                (house.suggest_ratio * house.review_num - 1) / (house.review_num - 1)
            )
        else:
            house.suggest_ratio = "%.2f" % (
                (house.suggest_ratio * house.review_num) / (house.review_num - 1)
            )
        house.review_num -= 1
        house.save()
        return super().destroy(request, *args, **kwargs)


class KeywordView(viewsets.ModelViewSet):
    permission_classes = [IsReadOnlyOrAdmin]
    serializer_class = KeywordSerializer
    queryset = Keyword.objects.all().order_by("key_type")

    def list(self, request, *args, **kwargs):
        key_choices = [
            ("INFRA", "내부"),
            ("ROOM", "룸컨디션"),
            ("SAFETY", "치안"),
            ("TRANSPORT", "교통"),
        ]
        queryset = self.get_queryset()
        grouped_data = {}
        for key_type, group in groupby(
            queryset, key=lambda obj: dict(key_choices).get(obj.key_type)
        ):
            grouped_data[key_type] = [
                {"description": obj.description, "icon_url": obj.icon_url, "pk": obj.pk}
                for obj in group
            ]

        return Response(grouped_data, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def address_area_multi_search(request, search):
    query_params = request.GET.copy()
    if search == "area":
        search_areas = query_params.pop("area")
        print(search_areas)
        houses = House.objects.filter(area__area_code__in=search_areas)
        print("area_house", houses.count())
        if not houses.exists():
            return Response(
                {"message": "no search result"}, status=status.HTTP_404_NOT_FOUND
            )
    elif search == "address":
        address = query_params.pop("address")[0]
        houses = House.objects.filter(address__contains=address)
        print("address", address)
        if not houses.exists():
            return Response(
                {"message": "no search result"}, status=status.HTTP_404_NOT_FOUND
            )
    else:
        return Response(
            {"message": "invalid search type"}, status=status.HTTP_400_BAD_REQUEST
        )

    query_list = dict()
    for query in query_params:
        check_query(query, query_params, query_list)
    if query_list:
        print("query existed")
        reviews = Review.objects.filter(**query_list)
        houses = houses.filter(reviews__in=reviews).distinct()

    serializer = HouseSerializer(
        instance=houses, many=True, context={"request": request}
    )
    data = serializer.data

    # 이거 그냥 다 주면 좋을 것 같은데
    if search == "area":
        data = {
            area_code: list(house)
            for area_code, house in groupby(data, key=lambda x: x["area_code"])
        }

    return Response(data, status=status.HTTP_200_OK)


class TestEmail(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        send_mail(
            "TEST",
            "THis is a test",
            settings.EMAIL_HOST_USER,
            ["hyukjun1111@gmail.com"],
            fail_silently=False,
        )
        return Response(status=status.HTTP_200_OK)

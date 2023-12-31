from django.shortcuts import render
from .serializers import (
    HouseSerializer,
    HouseSerializerSimple,
    AreaSerializer,
    AreaSerializerSimple,
    KeywordSerializer,
    ReviewSerializer,
    ReviewUpdateSerializer,
)
from rest_framework import viewsets
from .models import Area, House, Keyword, Review, ReviewImage
from rest_framework.response import Response
from itertools import groupby
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsWriterOrAdmin, IsReadOnlyOrAdmin
from rest_framework.decorators import api_view, permission_classes
import json
from .utils import slice_and_get_coordinates, check_query, calculate_suggest
from rest_framework.views import APIView
import logging

logger = logging.getLogger(__name__)

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
    permission_classes = [IsAuthenticated, IsReadOnlyOrAdmin]

    def get_queryset(self):
        return House.objects.all()

    # simple list는 허용됨
    def get_permissions(self):
        if self.action == "list" and "simple" in self.request.query_params:
            return []
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        query_params = request.query_params
        instance = self.get_queryset()
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
            house = self.get_queryset().get(pk=data)
            reviews = house.reviews.all()
            serializer = ReviewSerializer(
                reviews, many=True, context={"user": request.user}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            result = self.get_queryset().filter(address__contains=data)
            serializer = self.get_serializer(result, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == "list" and "simple" in self.request.query_params:
            return HouseSerializerSimple
        return self.serializer_class


# deprececated now search is used from multi search view but create is still used
class ReviewView(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsWriterOrAdmin]

    def get_queryset(self):
        return Review.objects.all()

    def list(self, request, *args, **kwargs):
        query_params = request.query_params
        query_set = self.get_queryset()
        if not query_params:
            serializer = self.get_serializer(
                query_set, many=True, context={"user": request.user}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        query_list = dict()

        for query in query_params:
            self.check_query(query, query_params, query_list)
        print(query_list)
        result = query_set.filter(**query_list)
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
            logging.debug("the file is FormData Format")
        except:
            data_dict = request.data

        address = data_dict.pop("address")
        house_queryset = House.objects.filter(address=address)
        suggest = data_dict.get("suggest")
        try:
            if house_queryset.exists():
                house_instance = house_queryset.first()

                if house_instance.reviews.filter(user=request.user).exists():
                    return Response(
                        {"message": "the user has already written the Review"},
                        status=status.HTTP_409_CONFLICT,
                    )
                # house 정보 수정
                calculate_suggest(house_instance, suggest, "add")
                house_instance.review_num += 1
                house_instance.save()
            else:
                if data_dict.get("suggest") == 1:
                    suggest_ratio = 1
                else:
                    suggest_ratio = 0
                area = Area.objects.get(area_code=data_dict.get("area"))
                address, lat, lng = slice_and_get_coordinates(address)
                house_instance = House.objects.create(
                    area=area,
                    address=address,
                    lat=lat,
                    lng=lng,
                    name=data_dict.get("name"),
                    suggest_ratio=suggest_ratio,
                )
                logging.debug("house created")

            # review 형식에 맞게 수정
            data_dict.pop("area")
            data_dict.pop("name")
            key_pk = data_dict.pop("keywords")
            keywords = Keyword.objects.filter(pk__in=key_pk)

            review_instance = Review.objects.create(
                user=request.user, house=house_instance, **data_dict
            )
            review_instance.keywords.set(keywords)
            logging.debug("revew created")
            image_data = request.FILES.get("image_data", None)
            if image_data:
                logging.debug("image_data was located")
                ReviewImage.objects.create(review=review_instance, image=image_data)
            else:
                logging.debug("no image located")
            review_instance.save()
            serializer = self.get_serializer(
                review_instance, context={"user": request.user}
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logging.debug(e, exc_info=True)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            data = request.data.get("json_data")
            data = json.loads(data)
        except:
            data = request.data
            print(type(data))
        print(data)
        instance = self.get_object()
        house = instance.house
        address = request.data.get("address")

        # changed address
        if house.address != address:
            calculate_suggest(house, instance.suggest, "delete")
            house.review_num -= 1
            house.save()
            if house.review_num == 0:
                house.delete()

            new_house = House.objects.filter(address=address)
            if new_house.exists():
                instance.house = new_house
                calculate_suggest(new_house, data.get("suggest"), "add")
                new_house.review_num += 1
                new_house.save()
            else:
                area = Area.objects.get(area_code=data.get("area"))
                name = data.get("name", None)
                address, lat, lng = slice_and_get_coordinates(address)
                suggest_ratio = 1 if data.get("suggest") else 0
                house_instance = House.objects.create(
                    area=area,
                    address=address,
                    lat=lat,
                    lng=lng,
                    name=name,
                    suggest_ratio=suggest_ratio,
                )
                instance.house = house_instance
        else:  # same address
            suggest = data.get("suggest")
            calculate_suggest(house, suggest, "change", instance.suggest)
            house.save()
        data.pop("area")
        data.pop("address")
        data.pop("name")

        image_data = request.FILES.get("image_data", None)
        try:
            image = instance.image
            if image_data:
                image.delete()
                ReviewImage.objects.create(review=instance, image=image_data)
            else:
                image.delete()
        except:
            if image_data:
                ReviewImage.objects.create(review=instance, image=image_data)

        serializer = ReviewUpdateSerializer(instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def partial_update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     house = instance.house
    #     data_dict = request.data
    #     context = {"user": request.user}
    #     suggest = data_dict.get("suggest", None)

    #     # 집 suggest_ratio 수정
    #     if suggest != None:
    #         if suggest == 1 and instance.suggest == 0:
    #             house.suggest_ratio = "%.2f" % (
    #                 (house.suggest_ratio * house.review_num + 1) / house.review_num
    #             )
    #         elif suggest == 0 and instance.suggest == 1:
    #             house.suggest_ratio = "%.2f" % (
    #                 (house.suggest_ratio * house.review_num - 1) / house.review_num
    #             )
    #         house.save()

    #     print(data_dict)
    #     serializer = ReviewSerializer(
    #         instance, data=data_dict, partial=True, context=context
    #     )
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    try:
        query_params = request.GET.copy()
        if search == "area":
            search_areas = query_params.pop("area")[0].split("_")
            print(search_areas)
            houses = House.objects.filter(area__area_code__in=search_areas)
            print("area_house", houses.count())
            if not houses.exists():
                return Response(
                    {"message": "no search result", "area": search_areas},
                    status=status.HTTP_404_NOT_FOUND,
                )
        elif search == "address":
            address = query_params.pop("address")[0]
            houses = House.objects.filter(address__contains=address)
            print("address", address)
            if not houses.exists():
                return Response(
                    {"message": "no search result", "address": address},
                    status=status.HTTP_404_NOT_FOUND,
                )
        elif search == "price":
            houses = House.objects.all()
        else:
            return Response(
                {"message": "invalid search type"}, status=status.HTTP_400_BAD_REQUEST
            )

        query_list = dict()
        check_query(query_params, query_list)

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
                area_name: list(house)
                for area_name, house in groupby(data, key=lambda x: x["area_name"])
            }

        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

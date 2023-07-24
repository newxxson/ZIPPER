from django.shortcuts import render
from .serializers import HouseSerializer, HouseSerializerSimple, AreaSerializer, KeywordSerializer, ReviewSerializer
from rest_framework import viewsets
from .models import Area, House, Keyword, Review
from rest_framework.response import Response
from itertools import groupby
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsWriterOrAdmin, IsReadOnlyOrAdmin
from rest_framework.decorators import api_view, permission_classes
# Create your views here.


#used to see houses related to each area, can specify area
class AreaView(viewsets.ModelViewSet):
    serializer_class = AreaSerializer
    queryset = Area.objects.all()
    permission_classes = [IsAuthenticated, IsReadOnlyOrAdmin]
    
    def list(self, request, *args, **kwargs):
        query_params = request.query_params

        if not query_params:
            return super().list(request, *args, **kwargs)
        
        areacode = query_params.get('area-code')
        instance = self.queryset.filter(area_code=areacode)
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

#1. retreive only coordinates and ratio
#2. retreive all the house instance => pagination not supported yet 
#3. retreive specific house instance with address(postal_code)
#4. retreive house matching to search parameter
class HouseView(viewsets.ModelViewSet):
    serializer_class = HouseSerializer
    lookup_field = 'address'
    queryset = House.objects.all()
    permission_classes = [IsAuthenticated, IsReadOnlyOrAdmin]

    #simple list는 허용됨
    def get_permissions(self):
        if self.action == 'list' and 'simple' in self.request.query_params:
            return []
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        query_params = request.query_params
        instance = self.queryset
        if not query_params:
            print('no query')
            serializer = self.get_serializer(instance, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif 'simple' in query_params:
            print('simple')
            serializer = self.get_serializer(instance, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise ValidationError('Invalid query parameter.')
    
    #주소를 물으면 집들을 리턴, pk를 특정하면 리뷰를 리턴
    def retrieve(self, request, *args, **kwargs):
        data = self.kwargs.get(self.lookup_field)
        if data.isnumeric():
            house = self.queryset.get(pk = data)
            reviews = house.reviews.all()
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            result = self.queryset.filter(address__contains = data)
            serializer = self.get_serializer(result, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        
    def get_serializer_class(self):
        if self.action == 'list' and 'simple' in self.request.query_params:
            return HouseSerializerSimple
        return self.serializer_class
    
  

class ReviewView(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated, IsWriterOrAdmin]

    def list(self, request, *args, **kwargs):
        query_params = request.query_params

        if not query_params:
            serializer = self.get_serializer(self.queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        query_list = dict()

        for query in query_params:
            self.check_query(query, query_params, query_list)
        print(query_list)
        result = self.queryset.filter(**query_list)
        serializer = self.get_serializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #용어를 정리할 필요가 있음
    def check_query(self, query, query_params, query_list):
        condition = query_params.get(query)
        print(query, type(query), condition, type(condition))
        if query == 'area':
            query_list['house__area__area_code'] = condition
        elif query == 'rent':
            if condition == 'jeon':
                query_list['rent_type'] = condition
            elif condition == 'monthly':
                query_list['rent_type'] = condition
        elif query == 'dlb':
            query_list['deposit__gte'] = int(condition)
        elif query == 'dub':
            query_list['deposit__lte'] = int(condition)
        elif query == 'mlb':
            query_list['monthly__gte'] = int(condition)
        elif query == 'mub':
            query_list['monthly__lte'] = int(condition)

    def create(self, request, *args, **kwargs):
        data_dict = request.data
        address = data_dict.get('address')

        house_queryset = House.objects.filter(address = address)
        if house_queryset.exists():
            house_instance = house_queryset.first()

            #house 정보 수정
            suggest_ratio = house_instance.suggest_ratio
            review_num = house_instance.review_num
            if data_dict['suggest'] == 1:
                print('suggesting')
                house_instance.suggest_ratio = (review_num * suggest_ratio + 1) / (review_num + 1)
            else:
                print('nosuggest')
                house_instance.suggest_ratio = (review_num * suggest_ratio) / (review_num + 1)
            house_instance.review_num += 1
            house_instance.save()

            #review 형식에 맞게 수정
            data_dict.pop('area')
            data_dict.pop('address')
            data_dict.pop('lat')
            data_dict.pop('lng')
            data_dict.pop('name')
            key_pk = data_dict.pop('keywords')
            keywords = Keyword.objects.filter(pk__in=key_pk)
            print(keywords)
            review_instance = Review.objects.create(
                user = request.user,
                house = house_instance,
                **data_dict
            )
            review_instance.keywords.set(keywords)
            review_instance.save()
            serializer = self.get_serializer(review_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if data_dict.get('suggest') == 1:
                suggest_ratio = 1
            else:
                suggest_ratio = 0
            area = Area.objects.get(area_code = data_dict.get('area'))
            house_instance = House.objects.create(
                area = area,
                address = data_dict.get('address'),
                lat = data_dict.get('lat'),
                lng = data_dict.get('lng'),
                name = data_dict.get('name'),
                suggest_ratio = suggest_ratio
            )
            print('house_created')
            
            data_dict.pop('area')
            data_dict.pop('address')
            data_dict.pop('lat')
            data_dict.pop('lng')
            data_dict.pop('name')
            key_pk = data_dict.pop('keywords')
            keywords = Keyword.objects.filter(pk__in=key_pk)
            

            review_instance = Review.objects.create(
                user = request.user,
                house = house_instance,
                **data_dict
            )
            review_instance.keywords.set(keywords)
            review_instance.save()
            serializer = self.get_serializer(review_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        house = instance.house
        data_dict = request.data

        suggest = data_dict.get('suggest')

        #집 suggest_ratio 수정 
        if suggest != None:
            if suggest == 1 and  instance.suggest == 0: 
                house.suggest_ratio = (house.suggest_ratio * house.review_num + 1) / house.review_num
            elif suggest == 0 and instance.suggest == 1:
                house.suggest_ratio = (house.suggest_ratio * house.review_num - 1) / house.review_num
            house.save()
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        house = instance.house
        if house.review_num == 1:
            print('destroy house')
            return super().destroy(request, *args, **kwargs)
        
        if instance.suggest:
            house.suggest_ratio = (house.suggest_ratio * house.review_num - 1) / (house.review_num - 1)
        else:
            house.suggest_ratio = (house.suggest_ratio * house.review_num) / (house.review_num - 1)
        
        house.review_num -= 1        
        house.save()
        return super().destroy(request, *args, **kwargs)
        

class KeywordView(viewsets.ModelViewSet):
    permission_classes = [IsReadOnlyOrAdmin]
    serializer_class = KeywordSerializer
    queryset = Keyword.objects.all().order_by('key_type')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('key_type')
        grouped_data = {}
        for key_type, group in groupby(queryset, key=lambda obj: obj.key_type):
            grouped_data[key_type] = [
                {
                    'description' : obj.description, 
                    'icon_url' : obj.icon_url, 
                    'pk' : obj.pk
                }
                for obj in group]

        return Response(grouped_data, status=status.HTTP_200_OK)
    



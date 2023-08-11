from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from zip.models import Review
from django.contrib.auth import get_user_model
from zip.serializers import ReviewSerializer, HouseSerializer, AreaSerializer, HouseSerializerSimple
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from zip.models import Area, Review, House
from rest_framework.authtoken.models import Token
from rest_auth.views import LoginView
import json
from .serializers import CustomUserPatchSerializer, CustomLoginSerializer


class UserConfigView(APIView):
    def post(self, request):
        User = get_user_model()
        data = request.data
        extra_fields = {
            'age': data.get('age'),
            'sex': data.get('sex'),
            'major': data.get('major'),
            'interested_areas' : data.get('interested_areas')
        }

        try:
            user = User.objects.create_user(
                email = data.get('email'),
                id = data.get('id'),
                nickname = data.get('nickname'),
                password = data.get("password"),
                **extra_fields)
            
            token = Token.objects.create(user=user)
            return Response({'message': 'User created', 'token': token.key}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': str(e)}, status=400)
        
    @permission_classes([IsAuthenticated])
    def patch(self, request):
        user = request.user
        data = request.data
        serializer = CustomUserPatchSerializer(user, data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @permission_classes([IsAuthenticated])
    def delete(self, request):
        user = request.user
        user.delete()


    
@api_view(['GET'])
def verify_id(request, id):
    user = get_user_model()
    if user.objects.filter(id = id).exists():
        return Response({ 'valid' : False }, status=status.HTTP_409_CONFLICT)
    else:
        return Response({ 'valid' : True }, status=status.HTTP_200_OK)

@api_view(['GET'])
def verify_nickname(request, nickname):
    user = get_user_model()
    if user.objects.filter(nickname = nickname).exists():
        return Response({ 'valid' : False }, status=status.HTTP_409_CONFLICT)
    else:
        return Response({ 'valid' : True }, status=status.HTTP_200_OK)
    

class UserInterestView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        user = request.user
        data = json.loads(request.body)
        if 'area_code' in data:
            area_code = data.get('area_code')
            area = Area.objects.get(area_code=area_code)
            user.interested_areas.add(area)
            user.save()
        elif 'house_pk' in data:
            house_pk = data.get('house_pk')
            house = House.objects.get(pk=house_pk)
            user.interested_houses.add(house)
            house.interest_num += 1
            house.save()
            user.save()
        else:
            return Response({'message': 'Invalid query parameter value'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'interest saved'}, status=status.HTTP_201_CREATED)
            
    def get(self, request, type):
        user = request.user
        if type == 'area':
            interested_houses = House.objects.filter(area__in=user.interested_areas.all())
            serializer = HouseSerializerSimple(interested_houses, many=True, context={'request':request})
        elif type == 'house':
            interested_houses = user.interested_houses.all()
            serializer = HouseSerializerSimple(interested_houses, many=True, context={'request':request})
        else:
            return Response({'message': 'Invalid query parameter value'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, type, pk):
        user = request.user
        if type == 'area':
            area = Area.objects.get(area_code = pk)
            user.interested_areas.remove(area)
            user.save()

        elif type == 'house':
            house = House.objects.get(pk = pk)
            user.interested_houses.remove(house)
            house.interest_num -= 1
            house.save()
            user.save()
        else:
            return Response({'message': 'Invalid query parameter value'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message' : 'delete successful'}, status=status.HTTP_204_NO_CONTENT)



#retreive user written reviews
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_review(request):
    user = request.user

    review = user.reviews.all()
    serializer = ReviewSerializer(review, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)





class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer


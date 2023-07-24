from rest_framework import serializers
from rest_framework.fields import empty
from .models import Area, House, Review, Keyword





class HouseSerializer(serializers.ModelSerializer):
    area_name = serializers.CharField(source='area.area_name')

    class Meta:
        model = House
        fields = [field.name for field in House._meta.get_fields()]
        fields.append('area_name')

class HouseSerializerSimple(serializers.ModelSerializer):
    img_urls = serializers.SerializerMethodField()  
    class Meta:
        model = House
        fields = ['id', 'name', 'lat', 'lng', 'suggest_ratio', 'img_urls']

    def get_img_urls(self, house):
        # Get all img_url values from linked reviews and return as a list
        reviews = house.reviews.all()
        return [review.img_url for review in reviews]

    


class AreaSerializer(serializers.ModelSerializer):
    house = serializers.SerializerMethodField()
    class Meta:
        model = Area
        fields = ['area_code', 'area_name', 'house']
    
    def get_house(self, area):
        houses = area.houses.all()
        return [{'name': house.name, 'pk' : house.pk} for house in houses]

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['key_type', 'description', 'icon_url', 'pk']
        
    
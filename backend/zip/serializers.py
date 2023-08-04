from rest_framework import serializers
from rest_framework.fields import empty
from .models import Area, House, Review, Keyword





class HouseSerializer(serializers.ModelSerializer):
    area_name = serializers.CharField(source='area.area_name')

    class Meta:
        model = House
        fields = ['area', 'address', 'lat', 'lng', 'name', 'review_num', 'interest_num', 'suggest_ratio']
        fields.append('area_name')

class HouseSerializerSimple(serializers.ModelSerializer):
    area_name = serializers.CharField(source='area.area_name')
    is_interested = serializers.SerializerMethodField()
    img_urls = serializers.SerializerMethodField()  
    rat_avg = serializers.SerializerMethodField()
    class Meta:
        model = House
        fields = ['id','address', 'name', 'lat', 'lng', 'suggest_ratio', 'img_urls', 'rat_avg', 'area_name', 'is_interested']

    def get_img_urls(self, house):
        # Get all img_url values from linked reviews and return as a list
        reviews = house.reviews.all()
        return [review.img_url for review in reviews]
    def get_rat_avg(self, house):
        reviews = house.reviews.all()
        total = 0
        for review in reviews:
            total += review.rating_overall
        return total // reviews.count()
    def get_is_interested(self, house):
        user = self.context['request'].user
        return house.interested_users.filter(id=user.id).exists()
    
        
    


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
        exclude = ['user']

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['key_type', 'description', 'icon_url', 'pk']
        
    
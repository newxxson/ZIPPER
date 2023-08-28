from rest_framework import serializers
from rest_framework.fields import empty
from .models import Area, House, Review, Keyword


class HouseSerializer(serializers.ModelSerializer):
    area_code = serializers.CharField(source="area.area_code")
    area_name = serializers.CharField(source="area.area_name")
    is_interested = serializers.SerializerMethodField()
    rat_avg = serializers.SerializerMethodField()

    class Meta:
        model = House
        fields = [
            "area_code",
            "area_name",
            "id",
            "address",
            "name",
            "lat",
            "lng",
            "review_num",
            "rat_avg",
            "suggest_ratio",
            "rat_avg",
            "is_interested",
        ]

    def get_is_interested(self, house):
        user = self.context["request"].user
        return house.interested_users.filter(id=user.id).exists()

    def get_rat_avg(self, house):
        reviews = house.reviews.all()
        total = 0
        for review in reviews:
            total += review.rating_overall
        return total // reviews.count()


class HouseSerializerSimple(serializers.ModelSerializer):
    area_name = serializers.CharField(source="area.area_name")
    img_urls = serializers.SerializerMethodField()
    rat_avg = serializers.SerializerMethodField()
    is_interested = serializers.SerializerMethodField()

    class Meta:
        model = House
        fields = [
            "area_name",
            "id",
            "address",
            "name",
            "lat",
            "lng",
            "suggest_ratio",
            "img_urls",
            "rat_avg",
            "is_interested",
        ]

    def get_img_urls(self, house):
        # Get all img_url values from linked reviews and return as a list
        reviews = house.reviews.all()
        image_urls = []
        for review in reviews:
            if review.image:
                image_urls.append(review.image.get_cloudfront_url)
        return image_urls

    def get_is_interested(self, house):
        user = self.context["request"].user
        return house.interested_users.filter(id=user.id).exists()

    def get_rat_avg(self, house):
        reviews = house.reviews.all()
        total = 0
        for review in reviews:
            total += review.rating_overall
        return total // reviews.count()


class AreaSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ["area_code", "area_name"]


class AreaSerializer(serializers.ModelSerializer):
    house = serializers.SerializerMethodField()

    class Meta:
        model = Area
        fields = ["area_code", "area_name", "house"]

    def get_house(self, area):
        houses = area.houses.all()
        return [{"name": house.name, "pk": house.pk} for house in houses]


class ReviewSerializer(serializers.ModelSerializer):
    selected_keywords = serializers.SerializerMethodField()
    is_user = serializers.SerializerMethodField()
    area_name = serializers.CharField(source="house.area.area_name", read_only=True)
    house_name = serializers.CharField(source="house.name", read_only=True)
    address = serializers.CharField(source="house.address", read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Review
        exclude = ["user", "keywords", "house"]

    def get_selected_keywords(self, review):
        keywords = review.keywords.all()
        return [
            {"description": keyword.description, "icon_url": keyword.icon_url}
            for keyword in keywords
        ]

    def get_is_user(self, review):
        if self.context["user"] == review.user:
            return True
        else:
            return False

    def get_image(self, review):
        if review.image:
            return review.image.get_cloudfront_url
        return None


class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ["user", "house"]


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ["key_type", "description", "icon_url", "pk"]

from typing import Any, Dict, Tuple
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


# Create your models here.
class House(models.Model):
    area = models.ForeignKey("Area", on_delete=models.PROTECT, related_name="houses")
    address = models.TextField(unique=True)
    lat = models.CharField(max_length=20)
    lng = models.CharField(max_length=20)
    name = models.CharField(max_length=100, blank=True, null=True)

    review_num = models.IntegerField(default=1)
    interest_num = models.IntegerField(default=0)
    suggest_ratio = models.FloatField()

    def __str__(self) -> str:
        if self.name is not None:
            return self.name
        else:
            return self.address


class Area(models.Model):
    area_code = models.TextField(unique=True, primary_key=True)
    area_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.area_name


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="reviews",
    )
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name="reviews")

    floor_choices = [("UP", "고층"), ("MID", "중층"), ("LOW", "저층"), ("UNDER", "반지하")]
    floor_type = models.CharField(max_length=10, choices=floor_choices)

    exit_year = models.IntegerField(null=True)

    house_choices = [
        ("OpenOneRoom", "오픈형 원룸"),
        ("SepOneRoom", "분리형 원룸"),
        ("OfficeTel", "오피스텔"),
        ("Duplex", "복층"),
        ("TwoRoom", "투룸"),
    ]
    house_type = models.CharField(
        max_length=20, choices=house_choices, default="OpenOneRoom"
    )
    rent_choices = [("monthly", "월세"), ("jeon", "전세")]
    rent_type = models.CharField(max_length=10)

    deposit = models.IntegerField()
    monthly = models.IntegerField(null=True)
    maintenance = models.IntegerField()

    keywords = models.ManyToManyField("Keyword", related_name="reviews", blank=True)

    merits = models.TextField()
    demerits = models.TextField()

    img_url = models.URLField(blank=True, null=True)

    rating_inside = models.IntegerField()
    rating_transport = models.IntegerField()
    rating_infra = models.IntegerField()
    rating_safety = models.IntegerField()
    rating_overall = models.IntegerField()

    suggest = models.BooleanField()

    def __str__(self):
        return self.house.__str__() + " review by " + self.user.__str__()

    def delete(self, using=None, keep_parents=False):
        has_other_reviews = (
            Review.objects.filter(house=self.house).exclude(pk=self.pk).exists()
        )

        if not has_other_reviews:
            self.house.delete()

        return super().delete(using, keep_parents)


class Keyword(models.Model):
    key_choices = [
        ("INFRA", "Infrastructure"),
        ("ROOM", "Room Condition"),
        ("SAFETY", "Safety"),
        ("TRANSPORT", "Transportation"),
    ]
    key_type = models.CharField(max_length=10, choices=key_choices)
    description = models.CharField(max_length=50)  # 방이 예뻐용

    icon_url = models.URLField()

    def __str__(self) -> str:
        return self.key_type + " / " + self.description

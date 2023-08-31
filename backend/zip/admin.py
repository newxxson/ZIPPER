from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import House, Area, Review, Keyword, ReviewImage

# Register your models here.


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list = [field.name for field in House._meta.get_fields()]


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list = [field.name for field in Area._meta.get_fields()]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list = [field.name for field in Review._meta.get_fields()]


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list = [field.name for field in Keyword._meta.get_fields()]


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list = [field.name for field in ReviewImage._meta.get_fields()]

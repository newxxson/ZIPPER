from rest_framework import serializers
from rest_auth.serializers import LoginSerializer
from .models import CustomUser
class CustomLoginSerializer(LoginSerializer):
    class Meta:
        fields = ('id', 'password')


class CustomUserPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['nickname', 'age', 'sex', 'major']

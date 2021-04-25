from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import  Group
from ..models import UserCategory
User = get_user_model()

class UserCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCategory
        fields = ('id',
        'category_name', 
        'description', 
        )
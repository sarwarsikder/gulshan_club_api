from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import  Group
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
        'username', 
        'email', 
        'image_medium',
        'image_thumbnail',
        "first_name", 
        "last_name", 
        "phone_primary",
        "phone_secondary",
        "club_ac_number",
        "category_name",
        "designation"
        "membership_date",
        "birthday",
        "marital_status",
        "marriage_anniversary",
        "spouse",
        "address",
        "nationality",
        "blood_group",
        "religion",
        "gender",
        "profession",
        "education",
        "opt"
        )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name", )
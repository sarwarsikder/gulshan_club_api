from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import  Group
from ..models import UserCategory
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    image_medium = serializers.SerializerMethodField('get_image_medium')
    image_thumbnail = serializers.SerializerMethodField('get_image_thumbnail')

    def get_image_medium(self, obj):
        if(obj.image_medium):
            return '%s%s' % (settings.MEDIA_URL, obj.image_medium)


    def get_image_thumbnail(self, obj):
        if (obj.image_thumbnail):
            return '%s%s' % (settings.MEDIA_URL, obj.image_thumbnail)

    class Meta:
        model = User
        ordering_fields = ['id', 'created_at']
        ordering = ['created_at']
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
        "designation",
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
        "opt",
        "status"
        )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name", )

class UserCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCategory
        fields = ('id',
        'category_name', 
        'description', 
        )
from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import  Group
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    image_medium = serializers.SerializerMethodField('get_image_medium')
    image_thumbnail = serializers.SerializerMethodField('get_image_thumbnail')

    def get_image_medium(self, obj):
        return '%s%s' % (settings.MEDIA_URL, obj.image_medium)

    def get_image_thumbnail(self, obj):
        return '%s%s' % (settings.MEDIA_URL, obj.image_thumbnail)

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
        "opt"
        )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name", )
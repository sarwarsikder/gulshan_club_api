from rest_framework import serializers
from  ..models import StuffUser



class UserStuffSerializer(serializers.ModelSerializer):
    class Meta:
        model = StuffUser
        fields = ('id',"mobile_number_primary","image_medium","image_thumbnail")
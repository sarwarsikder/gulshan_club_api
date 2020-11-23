from rest_framework import serializers
from  ..models import StuffUser



class UserStuffSerializer(serializers.ModelSerializer):
    class Meta:
        model = StuffUser
        fields = ('id','stuff_name', 'designation_group', "designation", "mobile_number_primary")
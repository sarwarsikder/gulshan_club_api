from django.contrib.auth.models import User
from ..models import StuffUser
import django_filters
from django.contrib.auth import get_user_model
User = get_user_model()


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', ]

class UserStuffFilter(django_filters.FilterSet):
    class Meta:
        model = StuffUser
        fields = ['stuff_name',]
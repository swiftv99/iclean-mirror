from django_filters.rest_framework import FilterSet

from apps.user.models import User


class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = {
            'email': ['icontains'],
            'role': ['exact'],
            'country': ['icontains'],
            'city': ['icontains'],
        }

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.notification import views


# Create a router and register our viewsets with it.
# router = DefaultRouter()
# router.register(r'notifications', views.NotificationViewSet,basename="notifications")

# The API URLs are now determined automatically by the router.
# urlpatterns = [
#     path('', include(router.urls)),
# ]

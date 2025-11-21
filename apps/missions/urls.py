from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MissionViewSet

router = DefaultRouter()
router.register(r'', MissionViewSet, basename='mission')

app_name = 'missions'

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CatViewSet

router = DefaultRouter()
router.register(r'', CatViewSet, basename='cat')

app_name = 'spy_cats'

urlpatterns = [
    path('', include(router.urls)),
]

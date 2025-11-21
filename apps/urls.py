"""
URL configuration for spycatagency project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Spy Cat Agency API",
      default_version='v1',
      description="API documentation for Spy Cat Agency management system",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/spy-cats/', include('apps.spy_cats.urls')),
    path('api/missions/', include('apps.missions.urls')),
    path('api/targets/', include('apps.targets.urls')),
    path('api/notes/', include('apps.notes.urls')),
    
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

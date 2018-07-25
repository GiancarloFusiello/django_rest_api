from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers

from restapi import views

router = routers.DefaultRouter()
router.register(r'prezis', views.PreziAPIView, base_name='prezis')

urlpatterns = [
    re_path(r'^api/', include(router.urls)),
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# Allow the admin browser view for devs
if settings.DEBUG:
    urlpatterns.append(
        path('admin/', admin.site.urls),
    )

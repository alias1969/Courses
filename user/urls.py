from django.urls import path, include
from rest_framework.routers import SimpleRouter

from user.apps import UserConfig

app_name = UserConfig.name

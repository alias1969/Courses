from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet

from user.apps import UserConfig

app_name = UserConfig.name

router = DefaultRouter()
router.register(r"payments", PaymentViewSet)
from user.views import UserCreateAPIView

urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserCreateAPIView.as_view(), name="register"),
]
urlpatterns += router.urls

from django.urls import path
from rest_framework.routers import SimpleRouter

from course.apps import CourseConfig
from course.views import (
    CourseViewSet,
    HomePageView,
    LessonCreateApiView,
    LessonDestroyApiView,
    LessonListApiView,
    LessonRetrieveApiView,
    LessonUpdateApiView,
    SubscriptionViewSet,
)

app_name = CourseConfig.name

router = SimpleRouter()
router.register("course", CourseViewSet, basename='course')

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("lessons/", LessonListApiView.as_view(), name="lessons-list"),
    path("lessons/<int:pk>", LessonRetrieveApiView.as_view(), name="lessons-retrieve"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lessons-create"),
    path(
        "lessons/<int:pk>/lesson-delete/",
        LessonDestroyApiView.as_view(),
        name="lesson-delete",
    ),
    path(
        "lessons/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lessons-update"
    ),
    path("subscription/", SubscriptionViewSet.as_view(), name="subscription"),
] + router.urls

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
)

app_name = CourseConfig.name

router = SimpleRouter()
router.register("courses", CourseViewSet)
urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("lessons/", LessonListApiView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>", LessonRetrieveApiView.as_view(), name="lessons_retrieve"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lessons_create"),
    path(
        "lessons/<int:pk>/delete/",
        LessonDestroyApiView.as_view(),
        name="lessons_delete",
    ),
    path(
        "lessons/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lessons_update"
    ),
]

urlpatterns += router.urls

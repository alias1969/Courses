from django.views.generic import TemplateView
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.viewsets import ModelViewSet

from course.models import Course, Lesson
from course.serializers import CourseSerializer, LessonSerializer
from user.permissions import IsModer, IsOwner


class HomePageView(TemplateView):
    template_name = "home.html"


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModer,)
        elif self.action == 'destroy':
            self.permission_classes = (~IsModer, IsOwner)
        elif self.action in ['update','retrieve']:
            self.permission_classes = (IsModer, IsOwner)
        else:
            self.permission_classes = (IsModer,)
        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    serializer_class = LessonSerializer

    def get_permissions(self):
        self.permission_classes = (~IsModer,)
        return super().get_permissions()


class LessonListApiView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_permissions(self):
        self.permission_classes = (IsModer, IsOwner)
        return super().get_permissions()


class LessonRetrieveApiView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_permissions(self):
        self.permission_classes = (IsModer, IsOwner)
        return super().get_permissions()


class LessonUpdateApiView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_permissions(self):
        self.permission_classes = (IsModer, IsOwner)
        return super().get_permissions()


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()

    def get_permissions(self):
        self.permission_classes = (~IsModer, IsOwner)
        return super().get_permissions()

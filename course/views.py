from django.views.generic import TemplateView
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    get_object_or_404,
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from course.models import Course, Lesson, Subscription
from course.paginators import ViewPagination
from course.serializers import (
    CourseSerializer,
    LessonSerializer,
    SubscriptionSerializer,
)
from user.permissions import IsModer, IsOwner


class HomePageView(TemplateView):
    template_name = "home.html"


class CourseViewSet(ModelViewSet):
    """Viewset для работы с курсами"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = ViewPagination

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        else:
            self.permission_classes = (IsModer,)
        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_queryset(self):
        """Выбирает только курсы текущего пользователя, кроме группы модератора"""
        if self.permission_classes != (IsModer | IsOwner,):
            return Course.objects.none()

        if self.request.user.groups.filter(name="moders").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)


class LessonCreateApiView(CreateAPIView):
    """API view для создания нового урока."""
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        """Привязывает создаваемый урок текущим пользователем."""
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

    def get_permissions(self):
        self.permission_classes = (~IsModer,)
        return super().get_permissions()


class LessonListApiView(ListAPIView):
    """API view для списка всех уроков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = ViewPagination

    def get_permissions(self):
        self.permission_classes = (IsModer | IsOwner,)
        return super().get_permissions()

    def get_queryset(self):
        """Выбирает только курсы текущего пользователя, кроме группы модератора"""
        if self.permission_classes != (IsModer | IsOwner,):
            return Course.objects.none()

        if self.request.user.groups.filter(name="moders").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)


class LessonRetrieveApiView(RetrieveAPIView):
    """API view для урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_permissions(self):
        self.permission_classes = (IsModer | IsOwner,)
        return super().get_permissions()


class LessonUpdateApiView(UpdateAPIView):
    """API view для редактирования урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_permissions(self):
        self.permission_classes = (IsModer | IsOwner,)
        return super().get_permissions()


class LessonDestroyApiView(DestroyAPIView):
    """API view для удаления урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()


class SubscriptionViewSet(APIView):
    """эндпоинт для создания подписки на курс"""

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, request):
        """Создание или удаление подписки на курс"""
        user_id = request.user
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)
        sub_item = Subscription.objects.filter(user=user_id, course=course_item)

        if sub_item.exists():
            sub_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user_id, course=course_item)
            message = "Подписка добавлена"
        return Response({"message": message})

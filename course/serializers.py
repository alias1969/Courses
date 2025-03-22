from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField

from .models import Course, Lesson, Subscription
from .validators import url_validator


class LessonSerializer(ModelSerializer):
    """Serialize for lessons"""

    url = serializers.CharField(validators=[url_validator], read_only=True)

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    """Serialize for courses"""

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    """Serializer для детального представления курса"""

    count_of_lessons = SerializerMethodField()
    lesson_set = LessonSerializer(many=True, read_only=True)
    subscription_sign = SerializerMethodField()

    def get_count_of_lessons(self, instance):
        """Возвращает количество уроков в курсе"""
        #return instance.lesson_set.count()
        return Lesson.objects.filter(course=instance).count()

    def get_subscription_sign(self, instance):
        """Возвращает подписку на курс"""
        user = self.context.get("request").user
        subscription = Subscription.objects.filter(user=user, course=instance).exists()
        return subscription

    class Meta:
        model = Course
        fields = "__all__"


class SubscriptionSerializer(ModelSerializer):
    """Serializer for subscription"""

    class Meta:
        model = Subscription
        fields = "__all__"

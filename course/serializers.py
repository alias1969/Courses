from rest_framework import serializers

from .models import Course, Lesson, Subscription
from .validators import url_validator


class LessonSerializer(serializers.ModelSerializer):
    """Serialize for lessons"""
    url = serializers.CharField(validators=[url_validator], read_only=True)

    class Meta:
        model = Lesson
        fields = ["title", "url"]


class CourseSerializer(serializers.ModelSerializer):
    """Serialize for courses"""
    class Meta:
        model = Course
        fields = '__all__'


class CourseDetailSerializer(serializers.ModelSerializer):
    """Serializer для детального представления курса"""
    count_of_lessons = serializers.SerializerMethodField()
    lesson_set = LessonSerializer(many=True, read_only=True)
    subscription_sign = serializers.SerializerMethodField()

    def get_count_lessons(self, instance):
        """Возвращает количество уроков в курсе"""
        return instance.lesson_set.count()

    def get_subscription_sign(self, instance):
        """Возвращает подписку на курс"""
        user = self.context.get("request").user
        subscription = Subscription.objects.filter(user=user, course=instance).exists()
        return subscription

    class Meta:
        model = Course
        fields = (
            "title",
            "description",
            "owner",
            "count_of_lessons",
            "lesson_set",
            "subscription_sign",
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for subscription"""

    class Meta:
        model = Subscription
        fields = "__all__"

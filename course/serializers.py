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

    url = serializers.CharField(validators=[url_validator], read_only=True)

    count_of_lessons = serializers.SerializerMethodField()
    info_lessons = serializers.SerializerMethodField()

    def get_count_of_lessons(self, obj):
        return obj.lesson_set.count()

    def get_info_lessons(self, obj):
        lessons = obj.lesson_set.all()
        return LessonSerializer(lessons, many=True).data

    class Meta:
        model = Course
        fields = (
            "title",
            "description",
            "preview",
            "owner",
            "count_of_lessons",
            "info_lessons",
            "url",
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for subscription"""

    class Meta:
        model = Subscription
        fields = "__all__"

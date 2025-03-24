from webbrowser import Error

from django.urls import reverse
from rest_framework.test import APITestCase

from course.models import Course, Lesson, Subscription
from user.models import User

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


class TestCase(APITestCase):
    """Базовый класс для всех тестов"""

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.course = Course.objects.create(title="Test Course", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="Test Lesson", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)


class CourseTestCase(TestCase, APITestCase):
    """Тест для работы с курсами"""

    def test_course_retrieve(self):
        """Тестирование получения курса по ID"""
        url = reverse("course:course-detail", args=(self.course.pk,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], self.course.title)

    def test_course_create(self):
        """Тестирование создания нового курса"""
        url = reverse("course:course-list")
        data = {
            "title": "Test Course 2",
            "description": "Test description",
            "owner": self.user.pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Course.objects.count(), 2)

    def test_course_update(self):
        """Тестирование изменения курса по ID"""
        url = reverse("course:course-detail", args=(self.course.pk,))
        data = {
            "title": "Updated Test Course",
            "description": "Updated test description",
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Course.objects.get(pk=self.course.pk).title, "Updated Test Course"
        )

    def test_course_delete(self):
        """Тестирование удаления курса по ID"""
        url = reverse("course:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Course.objects.count(), 0)


class LessonTestCase(TestCase, APITestCase):
    """Тесты для работы с уроками"""

    def test_lesson_retrieve(self):
        """Тестирование получения урока по ID"""
        url = reverse("course:lessons-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], self.lesson.title)

    def test_lesson_create(self):
        """Тестирование создания нового урока"""
        url = reverse("course:lessons-create")
        data = {
            "title": "Test Lesson 2",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_update(self):
        """Тестирование изменения урока по ID"""
        url = reverse("course:lessons-update", args=(self.lesson.pk,))
        data = {
            "title": "Updated Test Lesson",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Lesson.objects.get(pk=self.lesson.pk).title, "Updated Test Lesson"
        )

    def test_lesson_delete(self):
        """Тестирование удаления урока по ID"""
        url = reverse("course:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscriptionTest(TestCase, APITestCase):
    """Тест для работы с подписками"""

    def test_subscription(self):
        url = reverse("course:subscription")
        data = {
            "user_id": self.user.pk,
            "course_id": self.course.pk,
        }

        # Проверка оформления подписки
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Подписка добавлена")

        class SubscriptionTest(TestCase, APITestCase):
            """
            Тесты для работы с подписками
            """

            def test_subscription(self):
                """
                Тест подписки на курс
                """
                url = reverse("course:subscription")
                data = {
                    "user_id": self.user.pk,
                    "course_id": self.course.pk,
                }

                # Проверка оформления подписки
                response = self.client.post(url, data=data)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json()["message"], "Подписка добавлена")

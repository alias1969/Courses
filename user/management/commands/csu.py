from django.core.management.base import BaseCommand
from django.template.defaultfilters import title

from course.models import Lesson, Course
from user.models import Payment, User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        params = dict(email="admin@sky.pro", password="123")
        user, user_status = User.objects.get_or_create(**params)

        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS("User created successfully."))

        course = Course.objects.create(
            title='Вводный',
            description='Вводный курс',
        )
        lesson = Lesson.objects.create(
            title='Вводный',
            description='Вводный курс',
            course=Course.objects.get(pk=course.pk)
        )

        Payment.objects.create(
            owner=user,
            payment_date="2024-12-01",
            course=Course.objects.get(pk=course.pk),
            lesson=None,
            amount=1000.00,
            type="CASH",
        )

        Payment.objects.create(
            owner=user,
            payment_date="2024-12-02",
            course=None,
            lesson=Lesson.objects.get(pk=lesson.pk),
            amount=2000.00,
            type="ONLINE",
        )

        self.stdout.write(self.style.SUCCESS("Данные о платежах загружены!"))

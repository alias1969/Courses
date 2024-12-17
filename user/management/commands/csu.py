from django.core.management.base import BaseCommand

from user.models import Payment, User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        params = dict(email="admin@sky.pro", password="123")
        user, user_status = User.objects.get_or_create(**params)

        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS("User created successfully."))

        Payment.objects.create(
            owner=user,
            payment_date="2024-12-01",
            paid_course_id=2,
            paid_lesson=None,
            amount=1000.00,
            type="CASH",
        )

        Payment.objects.create(
            owner=user,
            payment_date="2024-12-02",
            paid_course=None,
            paid_lesson_id=3,
            amount=2000.00,
            type="ONLINE",
        )

        self.stdout.write(self.style.SUCCESS("Данные о платежах загружены!"))

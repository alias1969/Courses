from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from course.models import Lesson, Course

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="почта", help_text="Введите почту"
    )

    phone = models.CharField(
        max_length=35,
        verbose_name="телефон",
        help_text="Введите номер телефона",
        **NULLABLE,
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="аватар",
        help_text="Загрузите аватар",
        **NULLABLE,
    )
    town = models.CharField(
        max_length=35,
        verbose_name="город",
        help_text="Введите название города",
        **NULLABLE,
    )
    token = models.CharField(max_length=100, verbose_name="Token", **NULLABLE)

    is_active = models.BooleanField(verbose_name="активный пользователь")
    last_login = models.DateTimeField(verbose_name="дата последнего входа", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_CHOICES = [
        ("ONLINE", "Банковский перевод"),
        ("CASH", "Наличными"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    date = models.DateField(default=datetime.now, verbose_name="Дата оплаты")
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        blank=True,
        null=True,
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        verbose_name="Урок",
        blank=True,
        null=True,
    )
    amount = models.DecimalField(decimal_places=2, max_digits=20, verbose_name="Сумма")
    type = models.CharField(
        max_length=50,
        choices=PAYMENT_CHOICES,
        verbose_name="Способ оплаты",
        default="Банковский перевод",
    )
    session_id = models.CharField(
        max_length=255,
        verbose_name="ID сессии",
        **NULLABLE,
    )
    link = models.URLField(
        max_length=400,
        verbose_name="Ссылка на оплату",
        **NULLABLE,
    )
    status = models.CharField(
        max_length=50,
        verbose_name="Статус платежа",
        **NULLABLE,
    )

    def __str__(self):
        return f"{self.owner} - {self.get_type_display()} - {self.amount}"

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"
        ordering = ["-date"]

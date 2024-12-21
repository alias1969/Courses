from django.db import models

NULLABLE = {"null": True, "blank": True}


class Course(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    description = models.TextField(
        verbose_name="Описание курса",
        help_text="Введите описание курса",
        **NULLABLE,
    )
    preview = models.ImageField(
        upload_to="course/previews",
        verbose_name="Превью",
        help_text="Загрузите превью",
        **NULLABLE,
    )
    owner = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        verbose_name='автор',
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    description = models.TextField(
        max_length=250,
        verbose_name="Описание урока",
        help_text="Введите описание урока",
        **NULLABLE,
    )
    picture = models.ImageField(
        upload_to="lms/pictures",
        verbose_name="Превью",
        help_text="Загрузите превью",
        **NULLABLE,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Выберите курс",
        related_name="lesson_set",
        **NULLABLE,
    )
    video_url = models.URLField(
        max_length=200,
        verbose_name="Ссылка на видео",
        help_text="Загрузите видео",
        **NULLABLE,
    )
    owner = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        verbose_name='автор',
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title

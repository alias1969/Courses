from django.contrib import admin

from course.models import Lesson


@admin.register(Lesson)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "title")

from django.contrib import admin

from user.models import User
from user.models import Course, Lesson, Payment

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Payment)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email")

from django.contrib import admin

# Register your models here.
from .models import Student, Faculty, Speciality, Mark


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        "last_name",
        "first_name",
        "faculty",
        "speciality",
    )


@admin.register(Faculty)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", )


@admin.register(Speciality)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "faculty")


@admin.register(Mark)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("mark_type", "student")



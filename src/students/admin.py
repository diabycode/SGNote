from django.contrib import admin

# Register your models here.
from .models import Student, Faculty, Speciality, Mark, Module, Lesson, Result, Semester


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
    list_display = ("student", "lesson", "semester", "mark_type", )


@admin.register(Module)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "faculty", "coefficient")


@admin.register(Lesson)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "coefficient")


@admin.register(Result)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("semester", "student", )


@admin.register(Semester)
class StudentAdmin(admin.ModelAdmin):
    pass
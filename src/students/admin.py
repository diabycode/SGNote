from django.contrib import admin

from .models import *


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        "last_name",
        "first_name",
        "faculty",
        "speciality",
    )


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("name", )


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ("name", "faculty", )


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ("student", "lesson", "semester", "mark_type", )


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("name", "faculty")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("name", "coefficient")


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    pass


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    pass

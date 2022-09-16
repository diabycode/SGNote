from django.contrib import admin

from .models import *


# Register your models here.
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("name", )


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ("name", "faculty", )


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
    list_display = (
        "semester_number",
        "academic_year",
    )

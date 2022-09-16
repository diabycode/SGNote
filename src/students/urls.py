from django.urls import path

from .views import *

app_name = "students"

urlpatterns = [
    path('', home, name="home"),
    path('list/', students_list, name="students_list"),
    path('faculties/', students_faculties, name="students_faculties"),
    path('modules/', students_modules, name="students_modules"),
    path('lessons/', students_lessons, name="students_lessons"),
    path('specialities/', students_specialities, name="students_specialities"),
    path('marks/', students_marks, name="students_marks"),

    path('create/', student_create_view, name="student_create"),

    path('module_dropdown/', module_dropdown, name="module_dropdown"),
    path('lesson_dropdown/', lesson_dropdown, name="lesson_dropdown"),
    path('semester_dropdown/', semester_dropdown, name="semester_dropdown"),
    path('specialities_dropdown/', specialities_dropdown, name="specialities_dropdown"),
]





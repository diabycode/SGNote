from django.urls import path

from .views import *

app_name = "departements_and_modules"

urlpatterns = [
    path('faculties/', students_faculties, name="students_faculties"),
    path('create_faculties/', create_faculties, name="create_faculties"),

    path('modules/', students_modules, name="students_modules"),
    path('create_modules/', create_modules, name="create_modules"),

    path('lessons/', students_lessons, name="students_lessons"),
    path('create_lessons/', create_lessons, name="create_lessons"),

    path('specialities/', students_specialities, name="students_specialities"),
    path('create_specialities/', create_specialities, name="create_specialities"),
]

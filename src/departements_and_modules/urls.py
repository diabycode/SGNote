from django.urls import path

from .views import *

app_name = "departements_and_modules"

urlpatterns = [
    path('faculties/', students_faculties, name="students_faculties"),
    path('modules/', students_modules, name="students_modules"),
    path('lessons/', students_lessons, name="students_lessons"),
    path('specialities/', students_specialities, name="students_specialities"),
]

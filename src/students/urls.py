from django.urls import path

from .views import *

app_name = "students"

urlpatterns = [
    path('list/', students_list, name="students_list"),
    path('details/<str:pk>/', students_details, name="students_details"),
    path('create/', student_create_view, name="student_create"),
    path('edit/<str:pk>/', student_edit, name="student_edit"),

    path('specialities_dropdown/', specialities_dropdown, name="specialities_dropdown"),
    path('level_dropdown/', level_dropdown, name="level_dropdown"),
]





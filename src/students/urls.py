from django.urls import path

from .views import *

app_name = "students"

urlpatterns = [
    path('', home, name="home"),
    path('list/', students_list, name="students_list"),
    path('details/<str:pk>/', students_details, name="students_details"),
    path('create/', student_create_view, name="student_create"),

    path('specialities_dropdown/', specialities_dropdown, name="specialities_dropdown"),
]





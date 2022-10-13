from django.urls import path

from .views import *

app_name = "marks_and_results"

urlpatterns = [
    path('marks/', students_marks, name="students_marks"),
    path('add_marks/', add_marks, name="add_marks"),
    path('add_marks/entering/', marks_entering, name="marks_entering"),
    path('add_marks/marks_saving/', marks_saving, name="marks_saving"),
    path('edit_mark/<str:pk>/', edit_mark, name="edit_mark"),
    path('results/', results, name="results"),

    path('module_dropdown/', module_dropdown, name="module_dropdown"),
    path('lesson_dropdown/', lesson_dropdown, name="lesson_dropdown"),
    path('semester_dropdown/', semester_dropdown, name="semester_dropdown"),
]
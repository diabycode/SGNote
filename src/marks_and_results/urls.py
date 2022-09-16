from django.urls import path

from marks_and_results.views import students_marks, module_dropdown, lesson_dropdown, semester_dropdown

urlpatterns = [
    path('marks/', students_marks, name="students_marks"),

    path('module_dropdown/', module_dropdown, name="module_dropdown"),
    path('lesson_dropdown/', lesson_dropdown, name="lesson_dropdown"),
    path('semester_dropdown/', semester_dropdown, name="semester_dropdown"),
]
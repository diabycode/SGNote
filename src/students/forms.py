import datetime

from django.forms import ModelForm
from django import forms

from .models import *


class StudentCreateForm(ModelForm):

    class Meta:
        model = Student
        fields = [
            "faculty",
            "speciality",
            "matricule",
            "first_name",
            "last_name",
            "birth",
        ]
        widgets = {
            "birth": forms.SelectDateWidget(
                years=(str(y) for y in range(1980, int(datetime.today().year)+1))
            ),
        }


class FacultyCreateForm(ModelForm):

    class Meta:
        model = Faculty
        fields = [
            "name",
        ]


class ModuleCreateForm(ModelForm):

    class Meta:
        model = Module
        fields = [
            "name",
            "faculty",
        ]


class SpecialityCreateForm(ModelForm):

    class Meta:
        model = Speciality
        fields = [
            "name",
            "faculty",
        ]


class LessonCreateForm(ModelForm):
    class Meta:
        model = Lesson
        fields = [
            "name",
            "coefficient",
            "module",
        ]





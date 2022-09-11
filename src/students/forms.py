import datetime

from django.forms import ModelForm
from django import forms

from students.models import Student


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
                years=(str(y) for y in range(1980, int(datetime.date.today().year)+1))
            ),
        }








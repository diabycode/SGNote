from django import forms
from dynamic_forms import DynamicField, DynamicFormMixin

from systems_and_levels.models import System
from .models import *


class StudentCreateForm(DynamicFormMixin, forms.Form):
    years = (str(i) for i in range(1985, int(datetime.today().year+1)))

    def get_speciality(self):
        return Speciality.objects.filter(faculty=self["faculty"].value())

    def get_level(self):
        return Level.objects.filter(system=self["system"].value())

    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all())
    speciality = DynamicField(forms.ModelChoiceField, queryset=get_speciality)
    system = forms.ModelChoiceField(queryset=System.objects.all())
    level = DynamicField(
        forms.ModelChoiceField,
        queryset=get_level,
    )
    matricule = forms.CharField(max_length=255, required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    birth = forms.DateField(widget=forms.SelectDateWidget(years=(y for y in years)), required=False)





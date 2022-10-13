from django import forms
from dynamic_forms import DynamicField, DynamicFormMixin

from systems_and_levels.models import System
from .models import *


class StudentCreateForm(DynamicFormMixin, forms.Form):
    genders = (
        ("m", "Maxcuclin"),
        ("f", "Feminin")
    )

    def get_speciality(self):
        return Speciality.objects.filter(faculty=self["faculty"].value())

    def get_level(self):
        return Level.objects.filter(system=self["system"].value())

    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all(), label="Faculté")
    speciality = DynamicField(forms.ModelChoiceField, queryset=get_speciality, label="Spécialité")
    system = forms.ModelChoiceField(queryset=System.objects.all(), label="Système")
    level = DynamicField(
        forms.ModelChoiceField,
        queryset=get_level,
        label="Niveau",
    )
    matricule = forms.CharField(max_length=255, required=True, label="Matricule")
    first_name = forms.CharField(max_length=150, required=True, label="Prénom")
    last_name = forms.CharField(max_length=150, required=True, label="Nom")
    gender = forms.ChoiceField(choices=genders, required=True, label="Genre")
    birth = forms.DateField(
        widget=forms.widgets.NumberInput(attrs={"type": "date"}),
        required=False,
        label="Naissance",
    )





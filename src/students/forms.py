import datetime

from django.forms import ModelForm
from django import forms
from dynamic_forms import DynamicField, DynamicFormMixin

from .models import *


class StudentCreateForm(DynamicFormMixin, forms.Form):
    years = (str(i) for i in range(1985, int(datetime.today().year+1)))

    def get_speciality(self):
        return Speciality.objects.filter(faculty=self["faculty"].value())

    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all())
    speciality = DynamicField(forms.ModelChoiceField, queryset=get_speciality)
    matricule = forms.CharField(max_length=255, required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    birth = forms.DateField(widget=forms.SelectDateWidget(years=(y for y in years)), required=False)


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


#  -----------------------
class SearchMarks(DynamicFormMixin, forms.Form):

    def get_modules(self):
        faculty = self["faculty"].value()
        return Module.objects.filter(faculty=faculty)

    def get_lessons(self):
        module = self["module"].value()
        return Lesson.objects.filter(module=module)

    def get_semesters(self):
        academic_year = self["academic_year"].value()
        return Semester.objects.filter(academic_year=academic_year)

    faculty = forms.ModelChoiceField(
        queryset=Faculty.objects.all(),
        initial=Faculty.objects.first()
    )

    module = DynamicField(
        forms.ModelChoiceField,
        queryset=get_modules,
    )

    lesson = DynamicField(
        forms.ModelChoiceField,
        queryset=get_lessons,
    )

    academic_year = forms.ModelChoiceField(
        queryset=AcademicYear.objects.all(),
        initial=AcademicYear.objects.last()
    )

    semester = DynamicField(
        forms.ModelChoiceField,
        queryset=get_semesters
    )



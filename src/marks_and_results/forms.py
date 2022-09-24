from django import forms
from dynamic_forms import DynamicFormMixin, DynamicField

from departements_and_modules.models import Module, Lesson, Faculty, Semester, AcademicYear


class SearchMarks(DynamicFormMixin, forms.Form):

    def get_modules(self):
        return Module.objects.filter(faculty=self["faculty"].value())

    def get_lessons(self):
        return Lesson.objects.filter(module=self["module"].value())

    def get_semesters(self):
        return Semester.objects.filter(academic_year=self["academic_year"].value())

    faculty = forms.ModelChoiceField(
        queryset=Faculty.objects.all(),
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
    )

    semester = DynamicField(
        forms.ModelChoiceField,
        queryset=get_semesters,
    )


class MarkCreaterForm(DynamicFormMixin, forms.Form):
    def get_modules(self):
        return Module.objects.filter(faculty=self["faculty"].value())

    def get_lessons(self):
        return Lesson.objects.filter(module=self["module"].value())

    def get_semesters(self):
        return Semester.objects.filter(academic_year=self["academic_year"].value())

    is_exam = forms.BooleanField(label="Cochez si cela est une note d'examen", required=False)

    faculty = forms.ModelChoiceField(
        queryset=Faculty.objects.all(),
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
    )

    semester = DynamicField(
        forms.ModelChoiceField,
        queryset=get_semesters,
    )




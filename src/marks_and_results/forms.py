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

    def get_initial_semester(self):
        return Semester.objects.filter(academic_year=self["academic_year"].value()).last()

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
        queryset=get_semesters,
        initial=get_initial_semester,
    )


class MarkCreaterForm(DynamicFormMixin, forms.Form):
    def get_modules(self):
        return Module.objects.filter(faculty=self["faculty"].value())

    def get_lessons(self):
        return Lesson.objects.filter(module=self["module"].value())

    def get_semesters(self):
        return Semester.objects.filter(academic_year=self["academic_year"].value())

    def get_initial_semester(self):
        return Semester.objects.filter(academic_year=self["academic_year"].value()).last()

    faculty = forms.ModelChoiceField(
        queryset=Faculty.objects.all(),
        initial=Faculty.objects.first(),
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
        queryset=get_semesters,
        initial=get_initial_semester,
    )




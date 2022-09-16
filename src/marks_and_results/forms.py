from django import forms
from dynamic_forms import DynamicFormMixin, DynamicField

from departements_and_modules.models import Module, Lesson, Faculty, Semester, AcademicYear


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

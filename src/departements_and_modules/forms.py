from django import forms
from dynamic_forms import DynamicField, DynamicFormMixin

from departements_and_modules.models import Faculty, Module, Speciality, Lesson, Semester, AcademicYear


class ModuleCreateForm(DynamicFormMixin, forms.Form):

    def get_semester(self):
        return Semester.objects.filter(academic_year=self["academic_year"].value())

    name = forms.CharField(max_length=100, label="Nom")
    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all())
    academic_year = forms.ModelChoiceField(queryset=AcademicYear.objects.all())
    semester = DynamicField(forms.ModelChoiceField, queryset=get_semester)


class FacultyCreateForm(forms.ModelForm):

    class Meta:
        model = Faculty
        fields = (
            "name",
            "system",
        )


class SpecilityCreateForm(forms.ModelForm):

    class Meta:
        model = Speciality
        fields = (
            "name",
            "faculty",
        )


class LessonCreateForm(forms.ModelForm):

    class Meta:
        model = Lesson
        fields = (
            "name",
            "coefficient",
            "module",
        )


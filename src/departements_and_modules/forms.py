from django.forms import ModelForm

from departements_and_modules.models import Faculty, Module, Speciality, Lesson


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

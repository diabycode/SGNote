from django.shortcuts import render

from .models import Faculty, Module, Lesson, Speciality
from .forms import FacultyCreateForm, ModuleCreateForm, LessonCreateForm, SpecialityCreateForm


def students_faculties(request):
    context = {
        "faculties": Faculty.objects.all(),
        "add_form": FacultyCreateForm,
    }

    if request.method == "POST":
        add_form = FacultyCreateForm(data=request.POST)
        if add_form.is_valid():
            add_form.save()
        else:
            context["add_form"] = FacultyCreateForm(initial={"name": request.POST["name"]})
    return render(request, "departements_and_modules/faculties.html", context=context)


def students_modules(request):
    context = {
        "modules": Module.objects.all(),
        "add_form": ModuleCreateForm,
    }
    if request.method == "POST":
        add_form = ModuleCreateForm(data=request.POST)
        if add_form.is_valid():
            add_form.save()
        else:
            context["add_form"] = ModuleCreateForm(initial={"name": request.POST["name"]})

    return render(request, "departements_and_modules/modules.html", context=context)


def students_lessons(request):
    context = {
        "lessons": Lesson.objects.all(),
        "add_form": LessonCreateForm,
    }
    if request.method == "POST":
        add_form = LessonCreateForm(data=request.POST)
        if add_form.is_valid():
            add_form.save()
        else:
            context["add_form"] = LessonCreateForm(initial={"name": request.POST["name"]})

    return render(request, "departements_and_modules/lessons.html", context=context)


def students_specialities(request):
    context = {
        "specialities": Speciality.objects.all(),
        "add_form": SpecialityCreateForm,
    }
    if request.method == "POST":
        add_form = SpecialityCreateForm(data=request.POST)
        if add_form.is_valid():
            add_form.save()
        else:
            context["add_form"] = SpecialityCreateForm(initial={"name": request.POST["name"]})
    return render(request, "departements_and_modules/specialities.html", context=context)


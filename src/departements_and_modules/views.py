from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ModuleCreateForm, FacultyCreateForm, SpecilityCreateForm, LessonCreateForm
from .models import Faculty, Module, Lesson, Speciality, AcademicYear


@login_required()
def students_faculties(request):
    context = {
        "faculties": Faculty.objects.all(),
        "now_academic_year": AcademicYear.objects.get(is_now_academic_year=True)
    }
    return render(request, "departements_and_modules/faculties.html", context=context)


@login_required()
def students_modules(request):
    context = {
        "modules": Module.objects.all(),
        "now_academic_year": AcademicYear.objects.get(is_now_academic_year=True)
    }
    return render(request, "departements_and_modules/modules.html", context=context)


@login_required()
def students_lessons(request):
    context = {
        "lessons": Lesson.objects.all(),
        "now_academic_year": AcademicYear.objects.get(is_now_academic_year=True)
    }
    return render(request, "departements_and_modules/lessons.html", context=context)


@login_required()
def students_specialities(request):
    context = {
        "specialities": Speciality.objects.all(),
        "now_academic_year": AcademicYear.objects.get(is_now_academic_year=True)
    }
    return render(request, "departements_and_modules/specialities.html", context=context)


# ---------- Create views ---------------------

@login_required()
def create_faculties(request):
    context = {}
    if request.method == "POST":
        form = FacultyCreateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            faculty = Faculty()
            faculty.name = data.get("name")
            faculty.system = data.get("system")

            faculty.save()
            return redirect("departements_and_modules:students_faculties")
    else:
        form = FacultyCreateForm()

    context["form"] = form
    return render(request,  "departements_and_modules/create_faculties.html", context=context)


@login_required()
def create_specialities(request):
    context = {}
    if request.method == "POST":
        form = SpecilityCreateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            speciality = Speciality()
            speciality.name = data.get("name")
            speciality.faculty = data.get("faculty")

            speciality.save()
            return redirect("departements_and_modules:students_specialities")
    else:
        form = SpecilityCreateForm()

    context["form"] = form
    return render(request,  "departements_and_modules/create_specialities.html", context=context)


@login_required()
def create_modules(request):
    context = {}
    if request.method == "POST":
        form = ModuleCreateForm(request.POST)
        if form.is_valid():
            datas = form.cleaned_data
            module = Module()
            module.name = datas.get("name")
            module.faculty = datas.get("faculty")
            module.academic_year = datas.get("academic_year")
            module.semester = datas.get("semester")

            module.save()
            return redirect("departements_and_modules:students_modules")
    else:
        form = ModuleCreateForm()

    context['form'] = form
    return render(request, "departements_and_modules/create_modules.html", context=context)


@login_required()
def create_lessons(request):
    context = {}
    if request.method == "POST":
        form = LessonCreateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            lesson = Lesson()
            lesson.name = data.get("name")
            lesson.coefficient = data.get("coefficient")
            lesson.module = data.get("module")

            lesson.save()
            return redirect("departements_and_modules:students_lessons")
    else:
        form = LessonCreateForm()

    context["form"] = form
    return render(request,  "departements_and_modules/create_lessons.html", context=context)


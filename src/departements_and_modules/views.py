from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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


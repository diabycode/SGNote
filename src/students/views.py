from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from .models import Student, Faculty, Module, Lesson, Speciality


def home(request):
    return render(request, "students/home.html", context=context)


def students_list(request):
    context = {
        "students": Student.objects.all(),
    }

    return render(request, "students/list.html", context=context)


def students_faculties(request):
    context = {
        "faculties": Faculty.objects.all(),
    }

    return render(request, "students/faculties.html", context=context)


def students_modules(request):
    context = {
        "modules": Module.objects.all(),
    }

    return render(request, "students/modules.html", context=context)


def students_lessons(request):
    context = {
        "lessons": Lesson.objects.all(),
    }

    return render(request, "students/lessons.html", context=context)


def students_specialities(request):
    context = {
        "specialities": Speciality.objects.all(),
    }

    return render(request, "students/specialities.html", context=context)

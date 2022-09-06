from pprint import pprint

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Student, Faculty, Module, Lesson, Speciality, Mark, AcademicYear, Semester


def home(request):
    context = {}
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


def students_marks(request):
    context = {
        "marks": [],

        "all_lessons": Lesson.objects.all(),
        "academic_years": AcademicYear.objects.all(),
        "semesters": Semester.objects.all(),

        "lesson_selected": None,
        "academic_year_selected": None,
        "semester_selected": None,

    }

    if request.GET and request.GET["lesson"]:

        lesson_object = get_object_or_404(Lesson, slug=request.GET["lesson"])

        students = Student.objects.all()

        context["lesson_selected"] = lesson_object

        for student in students:
            s_marks = student.get_marks(lesson=lesson_object)
            if request.GET["semester"]:
                s_marks = s_marks.filter(semester=Semester.objects.get(pk=request.GET["semester"]))
                context["semester_selected"] = Semester.objects.get(pk=request.GET["semester"])

            if request.GET["academic_year"]:
                s_marks = s_marks.filter(academic_year=AcademicYear.objects.get(pk=request.GET["academic_year"]))
                context["academic_year_selected"] = AcademicYear.objects.get(pk=request.GET["academic_year"])

            context["marks"].append(
                {
                    "student": student,
                    "mark_types": [m.mark_type for m in s_marks],
                }
            )

    return render(request, "students/marks.html", context=context)

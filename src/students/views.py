from django.shortcuts import render

# Create your views here.
from pprint import pprint

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .forms import StudentCreateForm
from .models import *


def home(request):
    context = {}
    return render(request, "students/home.html", context=context)


def students_list(request):
    context = {
        "students": None,

        "all_faculties": Faculty.objects.all(),
        "faculty_selected": None,
    }

    students = Student.objects.all()

    if request.method == "POST":
        if request.POST["faculty"] != "__all__":
            students = students.filter(faculty=get_object_or_404(Faculty, slug=request.POST["faculty"]))

            context["faculty_selected"] = get_object_or_404(Faculty, slug=request.POST["faculty"])

    context["students"] = students
    return render(request, "students/list.html", context=context)


class StudentCreateView(CreateView):
    model = Student
    template_name = "students/student_create.html"
    form_class = StudentCreateForm
    success_url = reverse_lazy("students:students_list")



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

        "all_faculties": Faculty.objects.all(),
        "all_lessons": Lesson.objects.all(),
        "academic_years": AcademicYear.objects.all(),
        "semesters": Semester.objects.all(),

        "faculty_selected": None,
        "lesson_selected": None,
        "academic_year_selected": None,
        "semester_selected": None,

    }

    if request.GET and request.GET["lesson"] and request.GET["faculty"]:

        faculty_object = get_object_or_404(Faculty, slug=request.GET["faculty"])
        lesson_object = get_object_or_404(Lesson, slug=request.GET["lesson"])

        context["faculty_selected"] = faculty_object
        context["lesson_selected"] = lesson_object

        students = Student.objects.filter(faculty=faculty_object)

        for student in students:
            s_marks = Mark.objects.filter(lesson=lesson_object, student=student)
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

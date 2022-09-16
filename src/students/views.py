from django.shortcuts import render, redirect

# Create your views here.
from pprint import pprint

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

import students
from .forms import *
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
    return render(request, "students/faculties.html", context=context)


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

    return render(request, "students/modules.html", context=context)


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

    return render(request, "students/lessons.html", context=context)


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
    return render(request, "students/specialities.html", context=context)


def students_marks(request):
    context = {
        "marks": [],
        "form": SearchMarks(),
    }
    students = Student.objects.all()

    if request.GET:
        form = SearchMarks(request.GET)
        if form.is_valid():
            faculty_selected = get_object_or_404(Faculty, pk=request.GET["faculty"])
            lesson_selected = get_object_or_404(Lesson, pk=request.GET["lesson"])
            academic_year_selected = get_object_or_404(AcademicYear, pk=request.GET["academic_year"])
            semester_selected = get_object_or_404(Semester, pk=request.GET["semester"])

            students.filter(faculty=faculty_selected)
            for student in students:
                s_marks = Mark.objects.filter(
                    lesson=lesson_selected,
                    student=student,
                    academic_year=academic_year_selected,
                    semester=semester_selected,
                )
                context["marks"].append(
                    {
                        "student": student,
                        "mark_types": [m.mark_type for m in s_marks],
                    }
                )

    return render(request, "students/marks.html", context=context)


# created views
def student_create_view(request):
    context = {}

    if request.method == "POST":
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            student = Student(
                faculty=get_object_or_404(Faculty, pk=form["faculty"].value()),
                speciality=get_object_or_404(Speciality, pk=form["speciality"].value()),
                matricule=form["matricule"].value(),
                first_name=form["first_name"].value(),
                last_name=form["last_name"].value(),
                birth=form["birth"].value(),
            )
            student.save()
            return redirect("students:students_list")
    else:
        form = StudentCreateForm()

    context["form"] = form
    return render(request, "students/student_create.html", context=context)


# dropdowns
def module_dropdown(request):
    if request.GET["faculty"]:
        form = SearchMarks(request.GET)
        return HttpResponse(form["module"])
    return HttpResponse('<option value="" selected>---------</option>')


def lesson_dropdown(request):
    if request.GET["module"]:
        form = SearchMarks(request.GET)
        return HttpResponse(form["lesson"])
    return HttpResponse('<option value="" selected>---------</option>')


def semester_dropdown(request):
    if request.GET["academic_year"]:
        form = SearchMarks(request.GET)
        return HttpResponse(form["semester"])
    return HttpResponse('<option value="" selected>---------</option>')


def specialities_dropdown(request):
    if request.GET["faculty"]:
        form = StudentCreateForm(request.GET)
        return HttpResponse(form["speciality"])
    return HttpResponse('<option value="" selected>---------</option>')

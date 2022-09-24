from django.shortcuts import render, redirect

# Create your views here.
from pprint import pprint

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

import students
from departements_and_modules.models import Module, Lesson, AcademicYear, Semester
from marks_and_results.models import Mark
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


def students_details(request, pk):
    context = {}

    student = get_object_or_404(Student, pk=pk)

    # all
    academic_years = AcademicYear.objects.all()
    semesters = Semester.objects.all()

    # get request data
    if request.GET:
        request.session["academic_year_selected"] = request.GET.get("academic_year")
        request.session["semester_selected"] = request.GET.get("semester")

    # get academic_year
    ac_pk = request.session.get("academic_year_selected", None)
    academic_year_selected = get_object_or_404(AcademicYear, pk=ac_pk) if ac_pk else None
    if not academic_year_selected:
        academic_year_selected = academic_years.last()
    semesters = semesters.filter(academic_year=academic_year_selected)

    # get semester
    sem_pk = request.session.get("semester_selected", None)
    semester_selected = get_object_or_404(Semester, pk=sem_pk) if sem_pk else None
    if not semester_selected:
        semester_selected = semesters.last()

    student_faculty_modules = student.faculty.module_set.all()
    student_lessons = []
    for module in student_faculty_modules:
        lessons = Lesson.objects.filter(module=module)
        student_lessons.extend(lessons)

    student_marks = Mark.objects.filter(
        student=student,
        academic_year=academic_year_selected,
        semester=semester_selected
    )
    student_marks_mapped_lessons = []
    for lesson in student_lessons:
        marks_mapped_lesson = (lesson, [m for m in student_marks.filter(lesson=lesson)])
        student_marks_mapped_lessons.append(marks_mapped_lesson)

    marks_len = []
    for mark in student_marks_mapped_lessons:
        marks_len.append(len(mark[1]))
    max_len = max(marks_len)

    context["student"] = student
    context["student_marks"] = student_marks_mapped_lessons
    context["academic_years"] = academic_years
    context["semesters"] = semesters
    context["academic_year_selected"] = academic_year_selected
    context["semester_selected"] = semester_selected
    context["max_len"] = max_len

    return render(request, "students/students_details.html", context=context)


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


def specialities_dropdown(request):
    if request.GET["faculty"]:
        form = StudentCreateForm(request.GET)
        return HttpResponse(form["speciality"])
    return HttpResponse('<option value="" selected>---------</option>')

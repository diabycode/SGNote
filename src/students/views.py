from django.contrib.auth.decorators import login_required
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


@login_required()
def students_list(request):
    context = {
        "students": None,

        "all_faculties": Faculty.objects.all(),
        "faculty_selected": None,
        "now_academic_year": AcademicYear.objects.get(is_now_academic_year=True),
    }
    all_students = Student.objects.all()
    faculty_selected = None

    if request.method == "POST":
        # edit faculty selected in session
        request.session["students_list__faculty_selected"] = request.POST.get("faculty")

    if request.session.get("students_list__faculty_selected"):
        if request.session.get("students_list__faculty_selected") != "__all__":
            faculty_selected = get_object_or_404(Faculty, pk=request.session.get("students_list__faculty_selected"))
            all_students = all_students.filter(faculty=faculty_selected)

    context["students"] = all_students
    context["faculty_selected"] = faculty_selected
    return render(request, "students/list.html", context=context)


@login_required()
def students_details(request, pk):
    context = {
        "now_academic_year": AcademicYear.objects.get(is_now_academic_year=True),
    }

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

    student_marks = Mark.objects.order_by("is_exam").filter(
        student=student,
        academic_year=academic_year_selected,
        semester=semester_selected,
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
@login_required()
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


@login_required()
def student_edit(request, pk):
    context = {}
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        form = StudentCreateForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            print(data)
            print()

            student.faculty = data.get("faculty")
            student.speciality = data.get("speciality")
            student.actual_level = data.get("level")
            student.matricule = data.get("matricule")
            student.first_name = data.get("first_name")
            student.last_name = data.get("last_name")
            student.gender = data.get("gender")
            student.birth = data.get("birth")

            student.save()
            return redirect("students:students_list")
    else:
        initial = {
            "faculty": student.faculty,
            "speciality": student.speciality,
            "level": student.actual_level,
            "system": student.actual_level.system if student.actual_level else None,
            "matricule": student.matricule,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "gender": student.gender,
            "birth": student.birth
        }
        form = StudentCreateForm(initial=initial)

    context["form"] = form
    context["student"] = student
    return render(request, "students/student_edit.html", context=context)


@login_required()
def specialities_dropdown(request):
    if request.GET["faculty"]:
        form = StudentCreateForm(request.GET)
        return HttpResponse(form["speciality"])
    return HttpResponse('<option value="" selected>---------</option>')


@login_required()
def level_dropdown(request):
    if request.GET["system"]:
        form = StudentCreateForm(request.GET)
        return HttpResponse(form["level"])
    return HttpResponse('<option value="" selected>---------</option>')


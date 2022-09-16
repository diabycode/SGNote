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

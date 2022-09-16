from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from departements_and_modules.models import Faculty, Lesson, AcademicYear, Semester
from marks_and_results.forms import SearchMarks
from .models import Mark
from students.models import Student


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

    return render(request, "marks_and_results/marks.html", context=context)


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


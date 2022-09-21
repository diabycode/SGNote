from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from departements_and_modules.models import Faculty, Lesson, AcademicYear, Semester, Module
from marks_and_results.forms import SearchMarks, MarkCreaterForm
from .models import Mark
from students.models import Student


def students_marks(request):
    context = {
        "marks": [],
        "form": None,
    }
    form = SearchMarks()

    students = Student.objects.all()
    marks = []
    max_len = 0
    if request.GET:
        form = SearchMarks(request.GET)
        if form.is_valid():
            faculty_selected = get_object_or_404(Faculty, pk=request.GET["faculty"])
            lesson_selected = get_object_or_404(Lesson, pk=request.GET["lesson"])
            academic_year_selected = get_object_or_404(AcademicYear, pk=request.GET["academic_year"])
            semester_selected = get_object_or_404(Semester, pk=request.GET["semester"])

            form.fields.get("faculty").initial = faculty_selected
            form.fields.get("module").initial = lesson_selected.module
            form.fields.get("lesson").initial = lesson_selected
            form.fields.get("academic_year").initial = academic_year_selected
            form.fields.get("semester").initial = semester_selected

            students = students.filter(faculty=faculty_selected)
            for student in students:
                s_marks = Mark.objects.filter(
                    lesson=lesson_selected,
                    student=student,
                    academic_year=academic_year_selected,
                    semester=semester_selected,
                )
                marks.append(
                    {
                        "student": student,
                        "mark_types": [m.mark_type for m in s_marks],
                    }
                )

            max_len = len(marks[0]["mark_types"])
            for i in range(1, len(marks)):
                if len(marks[i]["mark_types"]) > max_len:
                    max_len = len(marks[i]["mark_types"])

    context["marks"] = marks
    context["max_len"] = max_len
    context["form"] = form
    return render(request, "marks_and_results/marks.html", context=context)


def add_marks(request):
    context = {"form": None}
    form = MarkCreaterForm()
    context["form"] = form
    return render(request, "marks_and_results/add_marks.html", context=context)


def marks_entering(request):
    context = {}
    if not request.method == "POST":
        return redirect("marks_and_results:add_marks")
    else:
        form = MarkCreaterForm(request.POST)
        if not form.is_valid():
            context["form"] = form
            return render(request, "marks_and_results/add_marks.html", context=context)

        mark_datas = form.cleaned_data
        students = Student.objects.filter(faculty=mark_datas.get("faculty"))

        context["faculty_selected"] = mark_datas.get("faculty")
        context["module_selected"] = mark_datas.get("module")
        context["lesson_selected"] = mark_datas.get("lesson")
        context["academic_year_selected"] = mark_datas.get("academic_year")
        context["semester_selected"] = mark_datas.get("semester")
        context["students"] = students

        context["form"] = form
    return render(request, "marks_and_results/marks_entering.html", context=context)


def marks_saving(request):
    if request.method == "POST":

        lesson_selected = get_object_or_404(Lesson, pk=request.POST["lesson"])
        academic_year_selected = get_object_or_404(AcademicYear, pk=request.POST["academic_year"])
        semester_selected = get_object_or_404(Semester, pk=request.POST["semester"])

        marks_mapped_students = [(e[0].split('_')[0], e[1]) for e in request.POST.items() if e[0].endswith("_mark")]
        if marks_mapped_students:
            for item in marks_mapped_students:
                mark = Mark()

                mark.mark_type = item[1] if item[1] else "0"
                mark.student = get_object_or_404(Student, pk=item[0])
                mark.lesson = lesson_selected
                mark.semester = semester_selected
                mark.academic_year = academic_year_selected

                if request.POST.get("is_exam") == "True":
                    mark.is_exam = True

                mark.save()
            return redirect("marks_and_results:students_marks")


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


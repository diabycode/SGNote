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

    # all
    faculties = Faculty.objects.all()
    modules = Module.objects.all()
    lessons = Lesson.objects.all()
    academic_years = AcademicYear.objects.all()
    semesters = Semester.objects.all()

    if request.GET:
        request.session["mark_falculty_selected"] = request.GET.get("faculty")
        request.session["mark_module_selected"] = request.GET.get("module")
        request.session["mark_lesson_selected"] = request.GET.get("lesson")
        request.session["mark_academic_year_selected"] = request.GET.get("academic_year")
        request.session["mark_semester_selected"] = request.GET.get("semester")

    # get faculty
    faculty_pk = request.session.get("mark_falculty_selected", None)
    faculty_selected = get_object_or_404(Faculty, pk=faculty_pk) if faculty_pk else None
    if not faculty_selected:
        faculty_selected = faculties.first()

    # get module
    modules = modules.filter(faculty=faculty_selected)
    module_pk = request.session.get("mark_module_selected", None)
    module_selected = modules.get(pk=module_pk) if module_pk else None

    if not module_selected:
        module_selected = modules.first()

    # get lesson
    lessons = lessons.filter(module=module_selected)
    lesson_pk = request.session.get("mark_lesson_selected", None)
    lesson_selected = lessons.get(pk=lesson_pk) if lesson_pk else None
    if not lesson_selected:
        lesson_selected = lessons.first()

    # get academic_year
    academic_year_pk = request.session.get("mark_academic_year_selected", None)
    academic_year_selected = academic_years.get(pk=academic_year_pk) if academic_year_pk else None
    if not academic_year_selected:
        academic_year_selected = academic_years.last()

    semesters = semesters.filter(academic_year=academic_year_selected)
    semester_pk = request.session.get("mark_semester_selected", None)
    semester_selected = semesters.get(pk=semester_pk) if semester_pk else None
    if not semester_selected:
        semester_selected = semesters.last()

    students = Student.objects.all()
    marks = []
    max_len = 0
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
                "marks": [m for m in s_marks.filter(is_exam=False)],
                "exam_mark": student.get_lesson_exam_mark(
                    lesson=lesson_selected,
                    semester=semester_selected,
                    academic_year=academic_year_selected
                ),
                "lesson_class_mean": student.get_class_mean(
                    lesson=lesson_selected,
                    semester=semester_selected,
                    academic_year=academic_year_selected
                ),
                "semester_mean": student.get_lesson_semester_mean(
                    lesson=lesson_selected,
                    semester=semester_selected,
                )
            }
        )

    max_len = len(marks[0]["marks"])
    for i in range(1, len(marks)):
        if len(marks[i]["marks"]) > max_len:
            max_len = len(marks[i]["marks"])

    context["marks"] = marks
    context["max_len"] = max_len

    context["faculties"] = faculties
    context["modules"] = modules
    context["lessons"] = lessons
    context["academic_years"] = academic_years
    context["semesters"] = semesters

    context["faculty_selected"] = faculty_selected
    context["module_selected"] = module_selected
    context["lesson_selected"] = lesson_selected
    context["academic_year_selected"] = academic_year_selected
    context["semester_selected"] = semester_selected

    return render(request, "marks_and_results/marks.html", context=context)


def add_marks(request):
    context = {"form": None}

    faculty = None
    module = None
    lesson = None
    academic_year = None
    semester = None
    if request.session.get("mark_falculty_selected"):
        faculty = get_object_or_404(Faculty, pk=request.session.get("mark_falculty_selected"))
        module = get_object_or_404(Module, pk=request.session.get("mark_module_selected"))
        lesson = get_object_or_404(Lesson, pk=request.session.get("mark_lesson_selected"))
        academic_year = get_object_or_404(AcademicYear, pk=request.session.get("mark_academic_year_selected"))
        semester = get_object_or_404(Semester, pk=request.session.  get("mark_semester_selected"))

    initial = {
        "faculty": faculty,
        "module": module,
        "lesson": lesson,
        "academic_year": academic_year,
        "semester": semester,
    }
    form = MarkCreaterForm(initial=initial)
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


def edit_mark(request, pk):
    context = {}
    mark = get_object_or_404(Mark, pk=pk)
    if request.method == "POST":
        mark.mark_type = request.POST.get("mark_type")
        mark.save()
        return redirect("marks_and_results:students_marks")
    context["mark"] = mark
    return render(request, "marks_and_results/edit_mark.html", context=context)


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


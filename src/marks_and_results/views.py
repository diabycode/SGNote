from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from departements_and_modules.models import Faculty, Lesson, AcademicYear, Semester, Module
from marks_and_results.forms import SearchMarks, MarkCreaterForm
from .models import Mark
from students.models import Student


@login_required()
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
        request.session["mark_falculty_selected"] = faculty_selected.pk

    # get module
    modules = modules.filter(faculty=faculty_selected)
    module_pk = request.session.get("mark_module_selected", None)
    module_selected = modules.get(pk=module_pk) if module_pk else None
    if not module_selected:
        module_selected = modules.first()
        request.session["mark_module_selected"] = module_selected.pk

    # get lesson
    lessons = lessons.filter(module=module_selected)
    lesson_pk = request.session.get("mark_lesson_selected", None)
    lesson_selected = lessons.get(pk=lesson_pk) if lesson_pk else None
    if not lesson_selected:
        lesson_selected = lessons.first()
        request.session["mark_lesson_selected"] = lesson_selected.pk

    # get academic_year
    academic_year_pk = request.session.get("mark_academic_year_selected", None)
    academic_year_selected = academic_years.get(pk=academic_year_pk) if academic_year_pk else None
    if not academic_year_selected:
        academic_year_selected = academic_years.get(is_now_academic_year=True)
        request.session["mark_academic_year_selected"] = academic_year_selected.pk

    # get semester
    semesters = semesters.filter(academic_year=academic_year_selected)
    semester_pk = request.session.get("mark_semester_selected", None)
    semester_selected = semesters.get(pk=semester_pk) if semester_pk else None
    if not semester_selected:
        semester_selected = semesters.last()
        request.session["mark_semester_selected"] = semester_selected.pk

    # marks getting
    marks = []
    students = Student.objects.filter(faculty=faculty_selected)
    for student in students:
        s_marks = student.get_marks(lesson=lesson_selected,
                                    academic_year=academic_year_selected,
                                    semester=semester_selected)
        marks.append({"student": student, "marks": s_marks})

    max_len = 0
    if marks:
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

    context["now_academic_year"] = academic_years.get(is_now_academic_year=True)

    return render(request, "marks_and_results/marks.html", context=context)


@login_required()
def add_marks(request):
    context = {"form": None}
    if request.method == "POST":
        # get data
        form = MarkCreaterForm(request.POST)

        # verifications
        if form.is_valid():
            # data cleaned
            data_cleaned = form.cleaned_data

            # if is an exam mark
            if data_cleaned.get("is_exam"):
                exam_marks = Mark.objects.filter(
                    lesson=get_object_or_404(Lesson, pk=data_cleaned["lesson"].pk),
                    academic_year=get_object_or_404(AcademicYear, pk=data_cleaned["academic_year"].pk),
                    semester=get_object_or_404(Semester, pk=data_cleaned["semester"].pk),
                    is_exam=True
                )
                # if exam mark already exist
                if exam_marks:
                    context["form"] = form
                    context["exam_mark_already_exist"] = \
                        "Cette faculté dispose déjà d'une note d'examen pour ce semestre"
                    return render(request, "marks_and_results/add_marks.html", context=context)
            # put datas in session and redirection
            request.session["mark_falculty_selected"] = data_cleaned.get("faculty").pk
            request.session["mark_module_selected"] = data_cleaned.get("module").pk
            request.session["mark_lesson_selected"] = data_cleaned.get("lesson").pk
            request.session["mark_academic_year_selected"] = data_cleaned.get("academic_year").pk
            request.session["mark_semester_selected"] = data_cleaned.get("semester").pk
            request.session["mark_is_exam"] = data_cleaned.get("is_exam")
            return redirect("marks_and_results:marks_entering")

    else:
        initial = {}
        if request.session.get("mark_falculty_selected"):
            initial = {
                "faculty": get_object_or_404(Faculty, pk=request.session.get("mark_falculty_selected")),
                "module": get_object_or_404(Module, pk=request.session.get("mark_module_selected")),
                "lesson": get_object_or_404(Lesson, pk=request.session.get("mark_lesson_selected")),
                "academic_year": get_object_or_404(AcademicYear, pk=request.session.get("mark_academic_year_selected")),
                "semester": get_object_or_404(Semester, pk=request.session.get("mark_semester_selected")),
            }

        form = MarkCreaterForm(initial=initial)

    context["form"] = form
    return render(request, "marks_and_results/add_marks.html", context=context)


@login_required()
def marks_entering(request):
    context = {}

    # getting datas
    initial = {
        "faculty": get_object_or_404(Faculty, pk=request.session.get("mark_falculty_selected")),
        "module": get_object_or_404(Module, pk=request.session.get("mark_module_selected")),
        "lesson": get_object_or_404(Lesson, pk=request.session.get("mark_lesson_selected")),
        "academic_year": get_object_or_404(AcademicYear, pk=request.session.get("mark_academic_year_selected")),
        "semester": get_object_or_404(Semester, pk=request.session.get("mark_semester_selected")),
        "is_exam": request.session.get("mark_is_exam"),
    }

    form = MarkCreaterForm(initial=initial)

    students = Student.objects.filter(faculty=initial["faculty"])

    context["faculty_selected"] = initial["faculty"]
    context["module_selected"] = initial["module"]
    context["lesson_selected"] = initial["lesson"]
    context["academic_year_selected"] = initial["academic_year"]
    context["semester_selected"] = initial["semester"]
    context["students"] = students

    context["form"] = form
    return render(request, "marks_and_results/marks_entering.html", context=context)


@login_required()
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


@login_required()
def edit_mark(request, pk):
    context = {}
    mark = get_object_or_404(Mark, pk=pk)
    if request.method == "POST":
        mark.mark_type = request.POST.get("mark_type")
        mark.save()
        return redirect("marks_and_results:students_marks")
    context["mark"] = mark
    return render(request, "marks_and_results/edit_mark.html", context=context)


@login_required()
def results(request):
    if not request.session.get("mark_falculty_selected", None):
        return redirect("marks_and_results:students_marks")

    context = {
        "now_academic_year": AcademicYear.objects.get(is_now_academic_year=True)
    }

    faculty_selected = get_object_or_404(Faculty, pk=request.session.get("mark_falculty_selected"))
    module_selected = get_object_or_404(Module, pk=request.session.get("mark_module_selected"))
    lesson_selected = get_object_or_404(Lesson, pk=request.session.get("mark_lesson_selected"))
    academic_year_selected = get_object_or_404(AcademicYear, pk=request.session.get("mark_academic_year_selected"))
    semester_selected = get_object_or_404(Semester, pk=request.session.get("mark_semester_selected"))

    students = Student.objects.filter(faculty=faculty_selected)

    student_results = []
    for student in students:
        lesson_class_mean = student.get_a_lesson_class_mean(lesson=lesson_selected, semester=semester_selected)
        lesson_exam_mark = student.get_a_lesson_exam_mark(lesson=lesson_selected, semester=semester_selected)
        lesson_semester_mean = student.get_a_lesson_semester_mean(lesson=lesson_selected, semester=semester_selected)
        semester_mean = student.get_semester_mean(semester=semester_selected)
        annual_mean = student.get_annual_mean(academic_year=academic_year_selected)

        student_results.append({
            "student": student,
            "lesson_class_mean": lesson_class_mean if lesson_class_mean else "NULL",
            "lesson_exam_mark": lesson_exam_mark if lesson_exam_mark else "NULL",
            "lesson_semester_mean": lesson_semester_mean if lesson_semester_mean else "NULL",
            "semester_mean": semester_mean if semester_mean else "NULL",
            "annual_mean": annual_mean if annual_mean else "NULL",
        })

    context["faculty_selected"] = faculty_selected
    context["module_selected"] = module_selected
    context["lesson_selected"] = lesson_selected
    context["academic_year_selected"] = academic_year_selected
    context["semester_selected"] = semester_selected
    context["student_results"] = student_results

    return render(request, "marks_and_results/results.html", context=context)


@login_required()
def module_dropdown(request):
    if request.GET["faculty"]:
        form = SearchMarks(request.GET)
        return HttpResponse(form["module"])
    return HttpResponse('<option value="" selected>---------</option>')


@login_required()
def lesson_dropdown(request):
    if request.GET["module"]:
        form = SearchMarks(request.GET)
        return HttpResponse(form["lesson"])
    return HttpResponse('<option value="" selected>---------</option>')


@login_required()
def semester_dropdown(request):
    if request.GET["academic_year"]:
        form = SearchMarks(request.GET)
        return HttpResponse(form["semester"])
    return HttpResponse('<option value="" selected>---------</option>')


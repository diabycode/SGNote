from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from departements_and_modules.models import Faculty, Speciality, Module, Lesson, AcademicYear
from students.models import Student


@login_required()
def index(request):
    context = {
        "nb_students": len(Student.objects.all()),
        "nb_faculties": len(Faculty.objects.all()),
        "nb_specialities": len(Speciality.objects.all()),
        "nb_modules": len(Module.objects.all()),
        "nb_lessons": len(Lesson.objects.all()),
        "now_academic_year": AcademicYear.objects.get(is_now_academic_year=True)
    }

    return render(request, "sg_note/home.html", context=context)


def edit_now_academic_year(request):
    context = {}
    if request.method == "POST":
        academic_year_selected = get_object_or_404(AcademicYear, pk=request.POST.get("now_academic_year"))
        academic_year_selected.is_now_academic_year = True
        academic_year_selected.save()
        return redirect("index")

    now_academic_year = AcademicYear.objects.get(is_now_academic_year=True)
    context["academic_years"] = AcademicYear.objects.all()
    context["now_academic_year"] = now_academic_year
    return render(request, "sg_note/edit_now_academic_year.html", context=context)

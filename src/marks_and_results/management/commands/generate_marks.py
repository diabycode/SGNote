import random

from django.core.management import BaseCommand

from departements_and_modules.models import Faculty, AcademicYear, Semester, Lesson, Module
from marks_and_results.models import Mark
from students.models import Student


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("number", type=int)

    def handle(self, *args, **options):
        number = options.get("number")
        if number:

            faculties = Faculty.objects.all()
            faculty_selected = faculties[random.randint(0, len(faculties)-1)]

            modules = Module.objects.filter(faculty=faculty_selected)
            module_selected = modules[random.randint(0, len(modules)-1)]

            lessons = Lesson.objects.filter(module=module_selected)
            lesson_selected = lessons[random.randint(0, len(lessons) - 1)]

            academic_year = AcademicYear.objects.last()

            semesters = academic_year.semester_set.all()
            semester_selected = semesters[random.randint(0, len(semesters) - 1)]

            students = Student.objects.filter(faculty=faculty_selected)
            if students:
                for student in students:
                    print(student)
                    for i in range(number):
                        mark = Mark()
                        mark.student = student
                        mark.lesson = lesson_selected
                        mark.mark_type = random.randint(5, 19)
                        mark.academic_year = academic_year
                        mark.semester = semester_selected

                        mark.save()
                        print(f"{mark.mark_type} / {mark.lesson} / {mark.semester} / {mark.academic_year}")
                    print("---------------------")
                print()
                print(f"{number} marks generated")
                print(f"faculty: {faculty_selected}")
                print(f"module: {module_selected}")
                print(f"lesson: {lesson_selected}")
                print(f"semester: {semester_selected}")
            else:
                print("Aucun étudiant")


import random

import faker
from django.core.management import BaseCommand

from departements_and_modules.models import Faculty, Speciality
from students.models import Student


def get_str(len_):
    pattern = "azertyuiopqsdfghjklmwxcvbn1234567890"
    str_ = ""
    for i in range(len_):
        alea_index = random.randint(0, len(pattern) - 1)
        str_ += pattern[alea_index]
    return str_


class Command(BaseCommand):
    help = "Create a certains number of 'Students' objects and save it in db"

    def add_arguments(self, parser):
        parser.add_argument("number", type=int, help="Number of students")

    def handle(self, *args, **options):
        number = options.get("number")
        if number:
            fk = faker.Faker("fr-FR")

            faculties = Faculty.objects.all()
            faculty_selected = faculties[random.randint(0, len(faculties) - 1)]

            specialities = Speciality.objects.filter(faculty=faculty_selected)
            speciality_selected = specialities[random.randint(0, len(specialities) - 1)]

            for i in range(number):
                student = Student()
                student.faculty = faculty_selected
                student.speciality = speciality_selected

                student.last_name = fk.last_name()
                student.first_name = fk.first_name()
                student.matricule = get_str(10).upper()
                student.birth = None

                student.save()

                print(student.first_name)
                print(student.last_name)
                print(student.matricule)
                print("-"*10)

            print()
            print(f"{number} Student(s) created")
            print(f"Faculty: {faculty_selected}")
            print(f"Speciality: {speciality_selected}")


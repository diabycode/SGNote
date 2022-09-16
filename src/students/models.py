from datetime import datetime

import django
from django.db import models
from django.utils.text import slugify

from departements_and_modules.models import Faculty, Speciality


class Student(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, null=True)

    matricule = models.CharField(max_length=255, primary_key=True, unique=True, verbose_name="Matricule")
    first_name = models.CharField(max_length=150, verbose_name="Prenom")
    last_name = models.CharField(max_length=150, verbose_name="Nom")
    birth = models.DateField(verbose_name="Naissance", blank=True, null=True)

    class Meta:
        verbose_name = "étudiant"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    def get_marks(self, lesson=None, semester=None, academic_year=None):
        marks = self.mark_set.all()
        if lesson:
            marks = marks.filter(lesson=lesson)
        if semester:
            marks = marks.filter(semester=semester)
        if academic_year:
            marks = marks.filter(academic_year=academic_year)

        return marks



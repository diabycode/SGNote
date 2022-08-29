from django.db import models


class Faculty(models.Model):
    name = models.CharField(max_length=200)


class Speciality(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)


class Student(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, null=True)

    matricule = models.CharField(max_length=255, primary_key=True, unique=True, verbose_name="Matricule")
    first_name = models.CharField(max_length=150, verbose_name="Prenom")
    last_name = models.CharField(max_length=150, verbose_name="Nom")
    birth = models.DateField(verbose_name="Naissance", blank=True, null=True)


class Mark(models.Model):
    mark_type = models.FloatField(verbose_name="Note")
    student = models.ForeignKey(Student, on_delete=models.CASCADE)


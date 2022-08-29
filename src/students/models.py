from django.db import models


class Faculty(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "facultée"

    def __str__(self):
        return f"{self.name}"


class Speciality(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "spécialitée"

    def __str__(self):
        return f"{self.name}({self.faculty})"


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


class Mark(models.Model):
    mark_type = models.FloatField(verbose_name="Note")
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "note"
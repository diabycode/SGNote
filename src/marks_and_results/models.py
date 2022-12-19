from django.db import models

# Create your models here.
from departements_and_modules.models import Lesson, Semester, AcademicYear
from students.models import Student


class Mark(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True)
    mark_type = models.FloatField(verbose_name="Note")
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, verbose_name="Semestre", null=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, null=True)
    is_exam = models.BooleanField(null=True, default=False, verbose_name="Cochez si cela est une note d'examen")

    def __str__(self):
        return f"{self.mark_type}"

    class Meta:
        verbose_name = "note"

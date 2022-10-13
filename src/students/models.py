from datetime import datetime

import django
from django.db import models

from departements_and_modules.models import Faculty, Speciality, Lesson
from systems_and_levels.models import Level


class Student(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Facultée")
    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, null=True, blank=True,
                                   verbose_name="Spécialitée")
    actual_level = models.ForeignKey(Level, on_delete=models.SET_NULL, blank=True, null=True,
                                     verbose_name="Niveau actuel")
    matricule = models.CharField(max_length=255, primary_key=True, unique=True, verbose_name="Matricule")
    first_name = models.CharField(max_length=150, verbose_name="Prénom")
    last_name = models.CharField(max_length=150, verbose_name="Nom")
    gender = models.CharField(max_length=20, verbose_name="Genre", null=True)
    birth = models.DateField(verbose_name="Naissance", blank=True, null=True)

    class Meta:
        verbose_name = "étudiant"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    def _get_marks(self, lesson=None, semester=None, academic_year=None, exclude_exam=False):
        marks = self.mark_set.all()
        if lesson:
            marks = marks.filter(lesson=lesson)
        if academic_year:
            marks = marks.filter(academic_year=academic_year)
        if semester:
            marks = marks.filter(semester=semester)
        if exclude_exam:
            marks = marks.filter(is_exam=False)
        return marks

    def _get_a_lesson_class_mean(self, lesson, semester):
        """ get student marks mean in a specific lesson and return it """

        mean = None
        marks = self._get_marks(lesson=lesson, semester=semester, exclude_exam=True)
        if marks:
            marks_total = 0
            for mark in marks:
                marks_total += float(mark.mark_type)
            mean = marks_total/len(marks)
        return mean

    def _get_a_lesson_exam_mark(self, lesson, semester, to_float=False):
        """ get student exam mark in a specific lesson and return it """

        exam_mark = None
        marks = self._get_marks(lesson=lesson, semester=semester)
        if marks:
            exam_mark = marks.get(is_exam=True) if marks.filter(is_exam=True) else None
            if exam_mark is not None and to_float:
                exam_mark = float(exam_mark.mark_type)
        return exam_mark

    def _get_a_lesson_semester_mean(self, lesson, semester):
        semester_mean = None
        class_mean = self._get_a_lesson_class_mean(lesson=lesson, semester=semester)
        if class_mean is not None:
            exam_mark = self._get_a_lesson_exam_mark(to_float=True, lesson=lesson, semester=semester)
            if exam_mark is not None:
                semester_mean = (class_mean * 40 + exam_mark * 60) / 100
        return semester_mean

    def _get_semester_mean(self, semester):
        pass

    def _get_annual_mean(self, academic_year):
        pass

    def get_marks(self, lesson=None, semester=None, academic_year=None):
        return self._get_marks(lesson=lesson, semester=semester, academic_year=academic_year)

    def get_a_lesson_class_mean(self, lesson, semester):
        return self._get_a_lesson_class_mean(lesson, semester)

    def get_a_lesson_exam_mark(self, lesson, semester):
        return self._get_a_lesson_exam_mark(lesson=lesson, semester=semester)

    def get_a_lesson_semester_mean(self, lesson, semester):
        return self._get_a_lesson_semester_mean(lesson, semester)

    def get_semester_mean(self, semester):
        return self._get_semester_mean(semester)

    def get_annual_mean(self, academic_year):
        return self._get_annual_mean(academic_year)


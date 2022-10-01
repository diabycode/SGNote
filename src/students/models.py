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

    def _get_lesson_class_mean(self, lesson, semester, academic_year):
        lesson_class_mean = 0

        marks = self.get_marks(lesson=lesson, semester=semester, academic_year=academic_year)
        marks = marks.filter(is_exam=False)
        if marks:
            marks_int = [float(m.mark_type) for m in marks]
            lesson_class_mean = sum(marks_int)/len(marks)
        return lesson_class_mean

    def _get_lesson_exam_mark(self, lesson, semester, academic_year, to_float=False):
        marks = self.get_marks(lesson=lesson, semester=semester, academic_year=academic_year)
        if marks:
            exam_mark = marks.filter(is_exam=True)
            if exam_mark:
                exam_mark = exam_mark[0]
                if to_float:
                    exam_mark = float(exam_mark.mark_type)
                return exam_mark
        return 0

    def _get_lesson_semester_mean(self, lesson, semester):
        semester_mean = 0
        class_mean = self._get_lesson_class_mean(lesson=lesson, semester=semester, academic_year=semester.academic_year)
        exam_mean = self._get_lesson_exam_mark(to_float=True, lesson=lesson, semester=semester, academic_year=semester.academic_year)
        semester_mean = (class_mean * 40 + exam_mean * 60) / 100
        return semester_mean

    def _get_semester_mean(self, semester):
        modules = self.faculty.module_set.all()
        lessons = []
        for module in modules:
            lessons.append(Lesson.objects.filter(module=module))

        means_coefficiented = []
        coefficient_count = .0
        for lesson in lessons:
            lesson_semester_mean = self._get_lesson_semester_mean(lesson=lesson, semester=semester)
            lesson_semester_mean_coefficiented = lesson_semester_mean*float(lesson.coefficient)

            means_coefficiented.append(lesson_semester_mean_coefficiented)
            coefficient_count += float(lesson.coefficient)
        semester_mean = sum(means_coefficiented)/coefficient_count
        return semester_mean

    def _get_annual_mean(self, academic_year):
        semesters = academic_year.semester_set.all()
        semesters_mean = []
        for semester in semesters:
            semester_mean = self._get_semester_mean(semester=semester)
            semesters_mean.append(semester_mean)
        annual_mean = sum(semesters_mean)/len(semesters)
        return annual_mean

    def get_class_mean(self, lesson, semester, academic_year):
        return self._get_lesson_class_mean(lesson, semester, academic_year)

    def get_lesson_exam_mark(self, lesson, semester, academic_year):
        return self._get_lesson_exam_mark(lesson, semester, academic_year)

    def get_lesson_semester_mean(self, lesson, semester):
        return self._get_lesson_semester_mean(lesson, semester)

    def get_semester_mean(self, semester):
        return self._get_semester_mean(semester)

    def get_annual_mean(self, academic_year):
        return self._get_annual_mean(academic_year)


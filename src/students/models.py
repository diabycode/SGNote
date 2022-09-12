from datetime import datetime

from django.db import models
from django.utils.text import slugify


class Faculty(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=130, blank=True, null=True)

    class Meta:
        verbose_name = "facultée"

    def __str__(self):
        return f"{self.name}"

    @property
    def students_count(self):
        return len(self.student_set.all())

    @property
    def modules_count(self):
        return len(self.module_set.all())

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Faculty, self).save(*args, **kwargs)


class Speciality(models.Model):
    name = models.CharField(max_length=100, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=130, blank=True, null=True)

    class Meta:
        verbose_name = "spécialitée"

    def __str__(self):
        return f"{self.name}"

    @property
    def students_count(self):
        return len(self.student_set.all())

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Speciality, self).save(*args, **kwargs)


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


class Module(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, verbose_name="Facultée")
    name = models.CharField(max_length=100, verbose_name="Nom", unique=True)
    slug = models.SlugField(max_length=130, blank=True, null=True)

    class Meta:
        verbose_name = "module"

    def __str__(self):
        return f"{self.name}"

    @property
    def lesson_count(self):
        return len(self.lesson_set.all())

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Module, self).save(*args, **kwargs)


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, verbose_name="Module")
    coefficient = models.FloatField(default=1, verbose_name="Coéfficient")
    name = models.CharField(max_length=100, verbose_name="Nom", unique=True)
    slug = models.SlugField(max_length=130, blank=True, null=True)

    class Meta:
        verbose_name = "lesson"

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Lesson, self).save(*args, **kwargs)


class AcademicYear(models.Model):
    semesters_number = models.IntegerField(default=2)
    bigin_date = models.DateField(verbose_name="Date début", default=datetime.today().date())
    end_date = models.DateField(verbose_name="Date fin")

    def __str__(self):
        if self.bigin_date and self.end_date:
            return f"{self.bigin_date.year} - {self.end_date.year}"
        else:
            return super().__str__()

    def save(self, *args, **kwargs):
        semesters = []
        for i in range(1, int(self.semesters_number)+1):
            semester = Semester()
            semester.semester_number = i
            semester.academic_year = self
            semesters.append(semester)
        super().save(*args, **kwargs)
        for semester in semesters:
            semester.save()

    class Meta:
        verbose_name = "année scolaire"


class Semester(models.Model):
    semester_number = models.IntegerField()
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "semestre"

    def __str__(self):
        return f"semestre {self.semester_number}"


class Mark(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True)
    mark_type = models.FloatField(verbose_name="Note")
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, verbose_name="Semestre", null=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "note"


from django.db import models


class System(models.Model):
    name = models.CharField(max_length=80, verbose_name="Système")


class Level(models.Model):
    name = models.CharField(max_length=80, verbose_name="Niveau")
    system = models.ForeignKey(System, on_delete=models.CASCADE, verbose_name="Système")



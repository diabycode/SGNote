from django.db import models


class System(models.Model):
    name = models.CharField(max_length=80, verbose_name="Système")

    class Meta:
        verbose_name = "Système"

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.CharField(max_length=80, verbose_name="Niveau")
    system = models.ForeignKey(System, on_delete=models.CASCADE, verbose_name="Système")

    class Meta:
        verbose_name = "Niveau"
        verbose_name_plural = "Niveaux"

    def __str__(self):
        return self.name



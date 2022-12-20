# Generated by Django 4.1 on 2022-10-06 01:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('departements_and_modules', '0004_remove_academicyear_semesters_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='semester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='departements_and_modules.semester', verbose_name='Semestre'),
        ),
        migrations.AlterField(
            model_name='module',
            name='faculty',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='departements_and_modules.faculty', verbose_name='Facultée'),
        ),
    ]
# Generated by Django 4.1 on 2022-08-29 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_semester_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='semester',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='students.semester', verbose_name='Semestre'),
        ),
        migrations.AlterField(
            model_name='result',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.student', verbose_name='Etudiant'),
        ),
    ]

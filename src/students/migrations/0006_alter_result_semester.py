# Generated by Django 4.1 on 2022-08-29 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_alter_result_semester_alter_result_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.semester', verbose_name='Semestre'),
        ),
    ]

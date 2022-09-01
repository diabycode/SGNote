# Generated by Django 4.1 on 2022-08-30 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_academicyear_delete_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='mark',
            name='academic_year',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='students.academicyear'),
        ),
        migrations.AddField(
            model_name='semester',
            name='academic_year',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='students.academicyear'),
        ),
    ]

# Generated by Django 4.1 on 2022-08-30 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0010_alter_academicyear_academic_year_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicyear',
            name='academic_year_end',
            field=models.IntegerField(verbose_name='year'),
        ),
        migrations.AlterField(
            model_name='academicyear',
            name='academic_year_start',
            field=models.IntegerField(verbose_name='year'),
        ),
    ]
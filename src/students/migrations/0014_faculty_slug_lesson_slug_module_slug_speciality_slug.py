# Generated by Django 4.1 on 2022-09-06 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0013_remove_module_coefficient'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='slug',
            field=models.SlugField(blank=True, max_length=130, null=True),
        ),
        migrations.AddField(
            model_name='lesson',
            name='slug',
            field=models.SlugField(blank=True, max_length=130, null=True),
        ),
        migrations.AddField(
            model_name='module',
            name='slug',
            field=models.SlugField(blank=True, max_length=130, null=True),
        ),
        migrations.AddField(
            model_name='speciality',
            name='slug',
            field=models.SlugField(blank=True, max_length=130, null=True),
        ),
    ]

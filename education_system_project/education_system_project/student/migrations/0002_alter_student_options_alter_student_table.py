# Generated by Django 5.0.2 on 2024-03-01 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={},
        ),
        migrations.AlterModelTable(
            name='student',
            table='students',
        ),
    ]

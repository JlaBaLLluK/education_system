# Generated by Django 5.0.2 on 2024-02-29 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='current_students_amount',
        ),
        migrations.AddField(
            model_name='group',
            name='current_students_amount',
            field=models.IntegerField(default=0),
        ),
    ]
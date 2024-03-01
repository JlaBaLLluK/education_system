# Generated by Django 5.0.2 on 2024-03-01 12:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_group_product_alter_lesson_product'),
        ('student', '0003_alter_student_available_product_alter_student_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='available_product',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students_on_product', to='product.product'),
        ),
        migrations.AlterField(
            model_name='student',
            name='group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students_in_group', to='product.group'),
        ),
    ]
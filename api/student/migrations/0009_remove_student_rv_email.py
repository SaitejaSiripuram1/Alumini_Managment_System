# Generated by Django 5.1.4 on 2024-12-27 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_alter_student_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='rv_email',
        ),
    ]

# Generated by Django 4.2.4 on 2023-09-15 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0025_students_join'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_dued',
            field=models.BooleanField(default=False),
        ),
    ]
# Generated by Django 4.2.4 on 2023-09-08 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_routine'),
    ]

    operations = [
        migrations.AddField(
            model_name='routine',
            name='week',
            field=models.TextField(blank=True),
        ),
    ]

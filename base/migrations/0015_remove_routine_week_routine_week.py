# Generated by Django 4.2 on 2023-09-08 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_alter_routine_sub'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='routine',
            name='week',
        ),
        migrations.AddField(
            model_name='routine',
            name='week',
            field=models.ManyToManyField(to='base.day'),
        ),
    ]
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  name = models.CharField(max_length=500)
  due_date = models.DateField(null=True, blank=True)
  number = models.CharField(max_length=100)
  logo = models.FileField(upload_to='logo')

  def __str__(self):
    return self.name


class SchoolInfo(models.Model):
  school = models.ForeignKey(User, on_delete=models.CASCADE)
  slogan = models.TextField(null=True, blank=True)
  facilities =  models.TextField(null=True, blank=True)
  admission = models.TextField(null=True, blank=True)
  address = models.TextField(null=True, blank=True)

class Gallery(models.Model):
  school = models.ForeignKey(User, on_delete=models.CASCADE)
  images = models.FileField(null=True, blank=True, upload_to='gallery')
  caption = models.TextField(null=True, blank=True)

class Notice(models.Model):
  title = models.CharField(max_length=200, null=True, blank=True)
  text = models.TextField(null=True, blank=True)
  date = models.DateField(null=True, blank=True)
  school = models.ForeignKey(User, on_delete=models.CASCADE)

class Subject(models.Model):
  school = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  name = models.CharField(max_length=200)
  code = models.CharField(max_length=200, null=True, blank=True)


class Class(models.Model):
  school = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  name = models.CharField(max_length=50)
  type = models.CharField(max_length=100)
  subjects = models.ManyToManyField(Subject)
  start_time = models.TimeField(null=True, blank=True)
  end_time = models.TimeField(null=True, blank=True)


class Section(models.Model):
  school = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  name = models.CharField(max_length=200)
  class_name = models.ManyToManyField(Class)
  shift = models.CharField(max_length=100)
  year = models.CharField(max_length=100)
  group = models.CharField(max_length=100)
  room = models.CharField(max_length=100)

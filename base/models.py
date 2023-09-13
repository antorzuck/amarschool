from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  name = models.CharField(max_length=500)
  due_date = models.DateField(null=True, blank=True)
  number = models.CharField(max_length=100)
  logo = models.FileField(upload_to='logo')

  def __str__(self):
    return self.name

class Principle(models.Model):
   school = models.ForeignKey(User, on_delete=models.CASCADE)
   name = models.CharField(max_length=100)
   image = models.FileField(upload_to='principle')
   message = models.TextField()

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
  clas_name = models.ForeignKey(Class, on_delete=models.CASCADE,null=True,blank=True)
  shift = models.CharField(max_length=100)
  year = models.CharField(max_length=100)
  group = models.CharField(max_length=100)
  room = models.CharField(max_length=100)

class Year(models.Model):
  year_name = models.CharField(max_length=100)
  

  def __str__(self):
    return str(self.year)


class Room(models.Model):
  school = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  room = models.CharField(max_length=50)
  desc = models.TextField(null=True, blank=True)




class Day(models.Model):
  name = models.CharField(max_length=50)
  def __str__(self):
        return self.name


class Routine(models.Model):
    school = models.ForeignKey(User, on_delete=models.CASCADE)
    clas = models.ForeignKey(Class, on_delete=models.CASCADE)
    sec = models.ForeignKey(Section, on_delete=models.CASCADE)
    period = models.CharField(max_length=100)
    sub = models.TextField(blank=True)
    start = models.TimeField()
    end = models.TimeField()
    week = models.ManyToManyField(Day)
    teacher = models.CharField(max_length=100)
    

    def __str__(self):
        return self.clas.name
    

    class Student(models.Model):
       name = models.CharField(max_length=500)
       image = models.FileField(upload_to='students')
       fname = models.CharField(max_length=100)
       mname = models.CharField(max_length=100)
       clas = models.ForeignKey(Class, on_delete=models.CASCADE)
       section = models.ForeignKey(Section, on_delete=models.CASCADE)
       roll = models.CharField(max_length=10000)
       due_date = models.DateField()
       blood = models.CharField(max_length=20)
       gender = models.CharField(max_length=20)
       




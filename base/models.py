from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  name = models.CharField(max_length=500)
  due_date = models.DateField(null=True, blank=True)
  number = models.CharField(max_length=100)
  logo = models.FileField(upload_to='logo')

  def __str__(self):
    return self.name



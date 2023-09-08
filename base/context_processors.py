from base.models import *

def get_subjects(r):
  context = {'subjects': Subject.objects.all()}
  return context

def get_classes(r):
  context = {'classes': Class.objects.filter(school__id=r.user.id)}
  return context

def get_years(r):
  context = {'years':Year.objects.all()}
  return context

def get_sec(r):
  context = {'sections':Section.objects.all()}
  return context

def get_day(r):
  context = {'days':Day.objects.all()}
  return context

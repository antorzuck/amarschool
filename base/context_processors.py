from base.models import Subject

def get_subjects(r):
  context = {'subjects': Subject.objects.all()}
  return context

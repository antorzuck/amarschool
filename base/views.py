from django.shortcuts import render, redirect
from django.http import JsonResponse
from base.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.decorators import api_view



def create_username(name):
  word = name
  if " " in word:
    word = word.replace(" ", "-")
  return word

def dashboard(request):
  return render(request, 'dashboard/home.html')


def home(request):
	return render(request, 'homecontent.html')

def register(request):
  if request.method == 'POST':
    name = request.POST.get('school')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    password = request.POST.get('p1')
    cp = request.POST.get('p2')
    username = create_username(name)

    if len(password) < 6:
      messages.warning(request, "Password must be 6 character long")
      return render(request, 'register.html')
    if User.objects.filter(email=email):
      messages.warning(request, "A user already exist with this email")
      return render(request, 'register.html')

    if password != cp:
      messages.warning(request, "Password not matched")
      return render(request, 'register.html')
    user = User.objects.create(name=name, username=username, email=email)
    user.set_password(password)
    user.save()
    return render(request,'register.html')

  return render(request, 'register.html')


def handle_login(request):
  if request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('pass')
    try:
      user = User.objects.get(email=email)
      print(user.username)
      print(password)
      auser = authenticate(request, username=user.username, password=password)
      print(auser)
      if auser is not None:
        login(request, auser)
        return redirect(dashboard)
      else:
        messages.warning(request, "User not found")
        return render(request, 'login.html')
    except:
      messages.warning(request, "User not found")
      return render(request, 'login.html')
  return render(request, 'login.html')


def handle_logout(request):
  logout(request)
  messages.success(request, "successfully logged out!")
  return redirect('/login')


def get_school(request, slug):

  try:
    school = User.objects.get(username=slug)
    schoolinfo = SchoolInfo.objects.get(school=school)
    p = Principle.objects.filter(school__username=slug)[0]
    print(p.name)
    notice = Notice.objects.filter(school=school).order_by('-id')
    context = {'school':school, 'info':schoolinfo,'notice':notice,'p':p}
    return render(request, 'schoolgov.html',context)
  except Exception as e:
    print(e)
    return redirect('/')


@api_view(['GET','POST'])
def pub_notice(request):
  data = request.data
  title = data.get('title')
  date = data.get('date')
  usr = data.get('usr')
  school = User.objects.get(username=usr)
  print(usr)
  print("*******")
  ntc = Notice.objects.create(school=school, date=date,title=title)
  ntc.save()
  return Response({'msg':'success'})



def class_info(request):
  if request.GET.get('delete'):
    try:
      sl = Class.objects.get(school=request.user, id=request.GET.get('delete'))
      sl.delete()
    except:
      return redirect(dashboard)

  data = request.POST
  clas = Class.objects.filter(school=request.user).order_by('-id')
  if request.method == 'POST':
    school = data.get('clg')
    name = data.get('name')
    type = data.get('type')
    subjects = data.getlist('subjects')
    start = data.get('start')
    end = data.get('end')
    cr = Class.objects.create(school=User.objects.get(username=school), name=name,type=type,start_time=start,end_time=end)
    cr.subjects.set(subjects)
 
    return JsonResponse({"msg":"success"})
  return render(request, 'dashboard/clas.html', context={'clas':clas})


def section(request):
  data = request.POST
  if request.method == "POST":
    cls = data.get('cls')
    s = Section.objects.create(clas_name=Class.objects.get(id=cls),school=User.objects.get(username=data.get('clg')),name = data.get('name'),group = data.get('group'),shift = data.get('shift'),year = data.get('year'),room=data.get('room'))
    s.save()
  sec = Section.objects.filter(school=request.user).order_by('-id')
  yr = request.GET.get('year')
  dl = request.GET.get('delete')
  if dl:
    dsc = Section.objects.get(school=request.user,id=dl).delete()
  if yr:
    sec = sec.filter(year=yr)
  context = {'sec':sec, 'yr':yr}
  return render(request, 'dashboard/section.html', context)

def get_rooms(request):
  data = request.POST
  rooms = Room.objects.filter(school=request.user).order_by('-id')
  context = {'rooms':rooms}
  if request.method == 'POST':
    r = Room.objects.create(
      school = User.objects.get(username=data.get('clg')),
      room = data.get('room'),
      desc = data.get('desc')
    )
    r.save()

  d = request.GET.get('delete')
  if d:
    try:
      Room.objects.get(school=request.user, id=d).delete()
    except:
      return redirect(dashboard)
  return render(request, 'dashboard/rooms.html', context)

def subject(request):
  data = request.POST
  d = request.GET.get('delete')
  if d:
    Subject.objects.get(id=d).delete()

  sub = Subject.objects.all()
  context = {'sub':sub}
  if request.method == 'POST':
    sc = User.objects.get(username=data.get('clg'))
    s = Subject.objects.create(school=sc,name=data.get('name'),code=data.get('code'))
    s.save()
  return render(request, 'dashboard/sub.html', context)


def routine(r):
  data = r.POST
  d = r.GET.get('delete')
  if d:
    Routine.objects.get(id=d).delete()
  context = {'routine': Routine.objects.all()}
  if r.method == 'POST':
    print(data.get('sub'))
    ru = Routine.objects.create(
     school = User.objects.get(username=data.get('clg')),
     clas = Class.objects.get(id=data.get('c')),
     sub = data.get('sub'),
     sec = Section.objects.get(id=data.get('s')),
     period = data.get('p'),
     start = data.get('st'),
     end = data.get('en'),
     teacher = data.get('t'))
    ru.week.set(data.getlist('d'))
  return render(r, 'dashboard/routine.html', context)


def view_routine(r):
  y = r.GET.get('year')
  cl = r.GET.get('class')
  s = r.GET.get('sec')
  routine= Routine.objects.all()

  if cl:
    routine = Routine.objects.filter(clas__name=cl)
  if s:
    routine = routine.filter(sec__name=s)

  context = {'y':y,'cl':cl,'se':s, 'routine':routine}
  return render(r,'dashboard/rv.html', context)


from django.http import QueryDict


def school_info(r):
  if r.method == 'POST':
    data = r.POST
    u = User.objects.get(username=data.get('clg'))
    u.name = data.get('name')
    u.number = data.get('number')
    u.username = data.get('un')
    if r.FILES.get('logo'):
      u.logo = r.FILES.get('logo')
    u.save()
  si = SchoolInfo.objects.get_or_create(school=r.user)
  p = Principle.objects.filter(school=r.user)[0]
  return render(r, 'dashboard/info.html',context={'p':p,'si':si})


def infoup(r):
  if r.method == 'POST':
    sx = SchoolInfo.objects.get_or_create(school__username=r.POST['clg1'])
    sx.slogan = r.POST['slogan']
    sx.facilities = r.POST['facilities']
    sx.address = r.POST['address']
    sx.admission = r.POST['addmission']
    sx.save()
  return JsonResponse({"msg":"eyy"})

def prin(r):
  if r.method == 'POST':
    p = Principle.objects.filter(school__username=r.POST.get('clg'))[0]
    p.name = r.POST.get('namep')
    if r.FILES.get('img'):
      p.image = r.FILES.get('img')
    p.message = r.POST.get('mess')
    p.save()
  return redirect('/')

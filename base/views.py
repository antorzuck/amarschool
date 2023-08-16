from django.shortcuts import render, redirect
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
        print("usrr have")
        l = login(request, auser)
        print(l)
        messages.success(request, "Logged in succesfull")
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
    notice = Notice.objects.filter(school=school).order_by('-id')
    context = {'school':school, 'info':schoolinfo,'notice':notice}
    return render(request, 'school.html',context)
  except Exception as e:
    print(e)
    print("***")
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


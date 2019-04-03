from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import user_SignUpForm,DocumentForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.core.mail import EmailMessage
from django.utils.timezone import localtime, now
from django.utils.timezone import datetime
from .models import Document
from background_task import background
from celery.schedules import crontab
import time
import schedule
from datetime import datetime, timedelta

def user_register(request):
    if request.method == 'POST':
        form = user_SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('upload')

        else:
            return render(request, 'todo/register.html', {'form': form})
    else:
        form =user_SignUpForm()
        return render(request, 'todo/register.html', {'form': form})


def  user_login(request):

    si=""
    if request.user.is_authenticated:
        job(request.user.username)
        return redirect('upload')

    elif request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if request.user.is_authenticated:
                return redirect('upload')
            else:
                s="incorret password"
                return render(request, 'todo/login.html', {'form': form,'si':s})
        else:
            return render(request, 'todo/login.html', {'form': form,'si':si})


    else:
        form = AuthenticationForm()
        return render(request, 'todo/login.html', {'form': form})

def pagelogout(request):
        logout(request)
        return redirect('http://127.0.0.1:8000/')

def upload(request):
  if request.user.is_authenticated:
    s = request.user.username
    a=""
    form = DocumentForm()
    today = datetime.strftime(datetime.now() - timedelta(0), '%Y-%m-%d')
    print(today)
    q = today.split("-")
    q1 = str(q[2]).split(" ")
    d = q[0] + "-" + q[1] + "-" + q[2]

    print(localtime(now()), "fassak")
    today = str(datetime.today())
    q = today.split(" ")
    h = str(q[1]).split(":")
    h = h[0] + ":" + h[1]
    if request.method == 'POST':

            print(a, "upload")
            b=Document()
            b.userid=s
            b.task=request.POST.get('task')
            b.date= request.POST.get('date')
            b.time= request.POST.get('time')
            x=request.POST.get('time')
            b.save()


            return render(request, 'todo/upload.html', {'form':form,'s':s,'l':a,'d':d,'h':h})

    else:
      form=DocumentForm()

      print("d",d)
      return render(request, 'todo/upload.html', {'form':form,'s':s,'l':a,'d':d,'h':h})
  else:
    return HttpResponse("<h1>please login to continue</h1>")


def files(request):
  if request.user.is_authenticated:
    s = request.user.username
    a = Document.objects.filter(userid=s).order_by('date','time')

    return render(request, 'todo/files.html', {'l':a})
  else:
    return HttpResponse("<h1>please login to continue</h1>")


def delete(request,usr,tid):
  if request.user.is_authenticated:
    s = request.user.username
    a = Document.objects.filter(todo_id=tid)
    if(len(a)>0):
     b=a[0]
    else:
        return redirect('files')

    if(b.userid==s):
        b.delete()
    return redirect('files')

  else:
    return HttpResponse("<h1>please login to continue</h1>")


def edit(request,usr,tid):
  if request.user.is_authenticated:
      s = request.user.username
      a = Document.objects.filter(todo_id=tid)

      if request.method == 'POST':
          b=a[0]
          b.userid = s
          b.task = request.POST.get('task')
          b.date = request.POST.get('date')
          b.time = request.POST.get('time')
          x = request.POST.get('time')
          b.save()
          return redirect('files')

      else:
          if (len(a) > 0):
              b = a[0]
          else:
              return redirect('files')
          if (b.userid == s):
              print(b.time,b.date,"hiiiiiiiiiiiiii")
              k=str(b.date)
              k=k.split("-")
              p=k[0]+"-"+k[1]+"-"+k[2]
              k = str(b.time)
              k = k.split(":")
              p1 = k[0] + ":" + k[1] + ":" + k[2]

              today = str(datetime.today())
              q = today.split("-")
              q1 = str(q[2]).split(" ")
              d = q[0] + "-" + q[1] + "-" + q[1]

              today = str(datetime.today())
              q = today.split(" ")
              h = str(q[1]).split(":")
              h = h[0] + ":" + h[1]
              return render(request, 'todo/edit.html', { 'l': b,'p':p,'p1':p1,'d':d})
          else:
              return redirect('files')
  else:
    return HttpResponse("<h1>please login to continue</h1>")


def status1(request,sta,usr,tid):
  if request.user.is_authenticated:
    s = request.user.username
    a = Document.objects.filter(todo_id=tid)
    if(len(a)>0):
     b=a[0]
    else:
        return redirect('files')

    if(b.userid==s):
        print("completeddddd")
        b.status=sta
        b.save()
    return redirect('files')

  else:
    return HttpResponse("<h1>please login to continue</h1>")


def contact(request):
  if request.user.is_authenticated:
        return render(request,'todo/about.html')

  else:
    return HttpResponse("<h1>please login to continue</h1>")

@background(schedule=1)
def job(uid):
    while(1):
     print("I'm working...")
     c=Document.objects.filter(userid=uid)
     x=User.objects.filter(username=uid)
     mail=x[0].email
     for b in c:
         k = str(b.date)
         k = k.split("-")
         print("kkk=",k)
         p = k[0] + "-" + k[1] + "-" + k[2]

         today = str(datetime.today())
         print(today)
         q = today.split("-")
         #print(q)
         q1 = str(q[2]).split(" ")
         d = q[0] + "-" + q[1] + "-" + q1[0]
         print("date=",d)
         print(k[0],q[0],k[1],q[1],k[2],"q",q1[0],"date")
         if(k[0]==q[0] and k[1]==q[1] and k[2]==q1[0]):
           k = str(b.time)
           k = k.split(":")
           p1 = k[0] + ":" + k[1] + ":" + k[2]

           today = str(datetime.today())
           q = today.split(" ")
           h = str(q[1]).split(":")
           h = h[0] + ":" + h[1]
           print(k,h,"time")
           if (k[0] == h[0] and k[1] == h[1] ):
               msg=b.task
               sub="todo upGrad"
               email = EmailMessage(sub, msg, to=[mail])
               email.send()
     time.sleep(30)

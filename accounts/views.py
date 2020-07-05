from django.shortcuts import render,redirect
from .forms import UserCustomCreationForm

from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
# Create your views here.
def index(request):
    return render(request,'accounts/index.html')


def signup(request):
    if request.method == 'POST':
        form = UserCustomCreationForm(request.POST)
        print(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request,user)
            return redirect('posts:index',request.user.username)
    else:
        form = UserCustomCreationForm()
    context = {
        'form': form,
    }
    return render(request,'accounts/signup.html',context)

def login(request):

    if request.method =='POST':
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            auth_login(request,form.get_user())

            return redirect('posts:index',request.user.username)

    else:
        form = AuthenticationForm()
    context={
        'form':form
    }
    return render(request,'accounts/login.html',context)


def logout(request):
    auth_logout(request)
    return redirect('accounts:index')
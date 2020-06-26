from django.shortcuts import render
from .forms import UserCustomCreationForm
from django.contrib.auth import login as auth_login
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
            return redirect('accounts:index')
    else:
        form = UserCustomCreationForm()
    context = {
        'form': form,
    }
    return render(request,'accounts/signup.html',context)
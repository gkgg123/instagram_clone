from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.forms import modelformset_factory
from .forms import PostForm,PostImageForm
from .models import PostImage
# Create your views here.
User = get_user_model()
def index(request,username):
    main_user = User.objects.get(username=username)
    posts = main_user.post.all()

    context = {
        'main_user' : main_user,
        'posts' : posts
    }
    return render(request,'posts/index.html',context)

def create(request,username):
    if request.user.username == username:
        if request.method == 'POST':
            form = PostForm(request.POST,request.FILES or None)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                if request.FILES:
                    for img in request.FILES.getlist('images'):
                        postimg = PostImage(post=post,image=img)
                        postimg.save()
                
                return redirect('posts:index',username)
        else:
            form = PostForm()

        context = {
            'form' : form,
        }
        return render(request,'posts/create.html',context)
    else:
        return redirect('posts:index',username)
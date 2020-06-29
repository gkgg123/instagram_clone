from django.shortcuts import render
from django.contrib.auth import get_user_model
# Create your views here.
User = get_user_model()
def index(request,username):
    main_user = User.objects.get(username=username)
    posts = main_user.post.all()
    print(posts)
    print(main_user.profile)
    context = {
        'main_user' : main_user,
        'posts' : posts
    }
    return render(request,'posts/index.html',context)
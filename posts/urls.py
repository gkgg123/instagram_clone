from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('<username>/',views.index,name='index'),
    path('<username>/create/',views.create,name='create')

]

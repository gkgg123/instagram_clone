from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail
# Create your models here.

def user_profile_path(instance,filename):
    return 'profile/{0}/{1}'.format(instance.username,filename)


class User(AbstractUser):
    nickname = models.CharField(max_length=10,verbose_name='닉네임')
    profile = models.ImageField(upload_to=user_profile_path,default='default/default_img.jpg',verbose_name='프로필 이미지')
    intro = models.TextField(verbose_name='한줄 소개',blank=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='followings')
    profile_thumbnail = ImageSpecField(source='profile',
                          processors=[Thumbnail(300, 300)],
                          format='JPEG',
                          options={'quality': 60})

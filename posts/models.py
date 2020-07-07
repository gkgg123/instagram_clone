from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail
# Create your models here.

class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='post')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='like_posts')


class PostComment(models.Model):
    content = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='postcomment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='like_comments')


def post_image_path(instance,filename):
    return 'profile/{0}/posts/{1}'.format(instance.post.user.username,filename)

class PostImage(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='postimage')
    image = models.ImageField(upload_to=post_image_path,verbose_name='포스트이미지')
    thumbnail = ImageSpecField(source='image',
                        processors=[Thumbnail(300, 300)],
                        format='JPEG',
                        options={'quality': 60})


class Tag(models.Model):
    name = models.CharField(max_length=50)
    posts = models.ManyToManyField(Post,related_name='tags')
from .models import Post,PostImage
from django import forms

class PostForm(forms.ModelForm):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = Post
        fields = ('content','images')

class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ('image',)


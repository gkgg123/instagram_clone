# README



### 1. 인스타그램 클론코딩

- 목표 : commit을 최대한 자세하게 작성하자
- 최대한 기능을 구현해보는데 노력하자
- 자세한 설명은 인스타그램클론코딩.md 파일 



### 2. 가상환경 개발

1. 가상환경 설치

   `python -m venv venv`

2. 가상환경 접속

   `source venv/Scripts/activate`

3. 패키지 설치

   `pip install -r requirements.txt`

4. 마이그레이션 하기

5. 서버 구동



### 3.구현상 처음써보거나 어려웠던 것

#### 3.1 account까지 만들면서 힘들었던 점(6/26일 까지)



- accounts에서 default 이미지경로랑 저장이미지경로 정하기

  ```python
  ### accounts/models.py
  def user_profile_path(instance,filename):
      return 'profile/{0}/{1}'.format(instance.username,filename)
  
  class User(AbstractUser):
      nickname = models.CharField(max_length=10,verbose_name='닉네임')
      profile = models.ImageField(upload_to=user_profile_path,default='default/default_img.jpg',verbose_name='프로필 이미지')
      intro = models.TextField(verbose_name='한줄 소개',blank=True)
      followers = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='followings')
  
  
  ```

  - 이미지경로를 저장할때, 들어오는 이미지파일을 임의의 경로로 저장할때에는 하나의 함수로 만들어서 저장할수 있다 위와 같이 하고 upload_to에 넣어주면 된다.
  - default할때에도 기본적인 위치는 media인걸로 생각을 하고 거기서 상대경로를 작성해주면 되었다.
  - `verbose_name`은 칼럼명을 내가 커스텀해서 정해주는것 같다. 
  - 위와 같이 할시, 그냥 templates에서 `{{form}}`을 해줄시 label에 들어가주는 이름이 바뀐다.

- css 파일을 변경했을때 사이트에서 제대로 적용안되는 경우가 있다. 그 이유는 css를 브라우저에서는 이미 캐싱을 해놓고 저장을 해놓은상태이기 때문에 해결방법은 두가지가 있다.

  - css 파일을 변경할때마다, css파일명을 다르게 한다. 그러면, 브라우저는 새로운 css파일인걸로 감지하기 때문에 새로 다운을 받는다.
  - 위와 같은 방법은 매번 바꿔야하는 귀차니즘때문에 하기 싫어진다. 그래서 내가 사용한 방법은 `ctrl`+`shift`+`r`로 강제 새로고침을 해주면, css파일을 다시 다운받기 때문에 css파일명을 굳이 바꿀필요는 없어진다.

- css에서 처음 써본 기능

  ```css
    -webkit-transition:opacity 2s ease-in;
    transition:opacity 2s ease-in;
  ```

  - 애니메이션 효과로 천천히 전화되는걸 보여주는것이다.
  - 바뀔 값을 정해주고 그 시간을 정해주는 것 같다.
  - css가 가장 어려운 것 같다.

##### 3.1.1 accounts에 더 추가할 기능들

- 현재는 사이트의 뼈대만 만들어놓고 꾸민 것이라, 아직 빠진 부분이 많다.
  - 먼저 follower를 구현을 안해놨다. model에 정의는 해놨지만 나중에 사용자 화면을 꾸밀때 follow 기능을 그때 추가할 것같다.
  - 프로필 페이지와 프로필 변경 페이지를 아직 안 만들었다.
    - 프로필 페이지에는 그 밑에 Post들이 들어가야하므로, 아직 안 만들어 놨다.  Post를 만들면서 같이 만들 것 같다.
    - 프로필 변경페이지도, 메인화면에서  Navbar에서 들어갈 예정이라서 아직 안 만들어놨다.
  - 로그인이나 회원가입에 실패했을 떄 주는 message를 구현안해놨다.
  - 로그인이나 회원가입 로그아웃시 로그인유무를 추가안해놨다 그 부분들을 추가해줄것이다.



#### 3.2 Posts 기능을 만들면서 힘들었던 점(6/29일)

> 다중이미지를 구현하는데 힘들었다. 다중이미지를 구현하는방식에는 크게 2가지 방법이 있다.
>
> 1)장고가 제시하는 modelfactory 방식
>
> 2)input 태그를 multiple 속성을 줘서 여러 FILE을 받는 방법

##### 3.2.1 장고가 제시하는 modelfactory 방식으로 다중업로드를 구현하는 방법

- 1: N 관계의 Post와 PostImage라는 클래스 모델이 있다고 가정하겠다.
- 그리고 각각에 대응되는 PostForm과 PostImageForm이라는 클래스 모델이 있다고 가정을 하겠다.

```python
### views.py

from django.forms import modelformset_factory

def create(request):
# modelformset_factory 함수 사용(extra로 최대 업로드할 수 있는 이미지 개수 설정)
# modelformset_factory에 사용자하고자 하는 모델과 그리고 해당 form을 지정해서 넣을수 있다.
# form을 안 넣으면 Model을 기반으로 만든다.
ImageFormSet = modelformset_factory(PostImage, form=PostImageForm, extra=3)



if request.method == "POST":
    form = PostForm(request.POST, request.FILES)
    
    formset = ImageFormSet(request.POST, request.FILES, queryset=PostImage.objects.none())
    # form validation
    
    
    if form.is_valid() and formset.is_valid():
        post = form.save(commit=False)
        post.username = request.user
        post.save()
        for form in formset.cleaned_data:
            # user가 올린 데이터는 formset.cleand_data에 저장되어있다. 그래서 그 만큼 for문을 시키는거다.
            # 유저가 모든 이미지들을 업로드하지 않았을 경우 crash 방지
            if form:
                image = form['image']
                photo = Image(post=post, image=image)
                photo.save()
  
        return redirect('posts:index')
    else:
        print(form.errors, formset.errors)
else:
    # method가 POST가 아닌 경우, 즉 처음 stay_create url로 이동한 경우
    form = PostForm()
    ### PostImage.objects.none()을 넣어주는 이유로 추정하는 것은, 빈 쿼리셋을 만들어주기 위함인것 같다.
    # 만약 여러개의 이미지를 업로드를 하면 여러개의 쿼리셋이 생성이될것인데, 그럴때 빈 쿼리셋이 없으면, 추가되는데 에로사항이 발생할것이다. 그래서 먼저 커리셋을 빈객체로 만들어준것 같다.
    formset = ImageFormSet(queryset=PostImage.objects.none())
	context = {
        'form' : form,
        'formset' : formset
    }

return render(request, 'posts/create.html', context)
```

- 위와 같이 views.py에서 작업을 완료하면 html 문서에서도 받아주는 작업을 해줘야한다.

  ```html
  <form id="post_form" method="post" action="" enctype="multipart/form-data">
  
      {% csrf_token %}
  
  
  	{{form}}
   <!-- 여기서 formset을 쓸려면 management_form을 써줘야하고
  	그리고 formset을 우리가 설정한 extra개수만큼 진행할수 있도록 for문을 돌려준다.
  -->
      {{ formset.management_form }}
      {% for Imageform in formset %}
          {{ Imageform }}
      {% endfor %}
  
  
      <input type="submit" name="submit" value="Submit" />
  </form>
  ```

- 이렇게 해주면 다중이미지를 올려줄수 있다. 하지만 여기서의 문제점은, 이미지 업로드 버튼이 여러개가 생긴다는 문제이다.

- 그래서 나는 이 방식을 채택하지 않았다.



##### 3.2.2. input태그의 multiple 속성을 true를 이용한 방식

```python
### forms.py

class PostForm(forms.ModelForm):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = Post
        fields = ('content','images')
```

- 먼저 form을 만들때 PostImage를 넣어주기 위한 images라는 fields를 만들어줬다.
  - FileField는 장고가 제공해주는 File을 업로드해주기 위한 form이다.
  - 여기서 widget을 이용하여 `ClearableFileInput(attrs={'multiple': True})`을 해주었다. 
  - File을 여러개 올릴수 있도록 설정을 해준것이다.

```python
def create(request,username):
    if request.method == 'POST':
        ### Postform에 images를 만들어주었기 때문에 뒤에는 그냥 넣어줬다.
        ### 안그러면 is_valid를 통과하지 못한다.
        form = PostForm(request.POST,request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            ### 만약에 사용자가 보낸 image가 있다면,
            if request.FILES:
                ### 반복문을 돌려준다. getlist를 통해 사용자가 보낸 정보를 request.FILES에서 리스트로 뽑아내주고,
                for img in request.FILES.getlist('images'):
                    ### 1:N 관계를 설정해줘서 저장해주면 된다.
                    postimg = PostImage(post=post,image=img)
                    print(postimg)
                    postimg.save()
            
            return redirect('accounts:login')
    else:
        form = PostForm()

    context = {
        'form' : form,
    }
    return render(request,'posts/create.html',context)
```

- 위와 같이 간략하게 만들수 있다.

```html
<form id="post_form" method="post" action="" enctype="multipart/form-data">
  {% csrf_token %}
  {{form}}

  <input type="submit" name="submit" value="Submit" />
```

- 그리고  form도 그냥 평소처럼 만들어주면, 이미지를 올릴수 있게된다. 대신 여러개의 파일을 올릴수 있도록 바뀌어진다.





##### 3.2.3 이미지 미리보여주기

```html
  <div id="carouselExampleControls" class="carousel slide" data-ride="carousel" style="width: 300px;">
    <div class="carousel-inner">
    </div>
    <a class="carousel-control-prev" href="#carouselExampleControls" role="button" data-slide="prev">
      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      <span class="sr-only">Previous</span>
    </a>
    <a class="carousel-control-next" href="#carouselExampleControls" role="button" data-slide="next">
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="sr-only">Next</span>
    </a>
  </div>
```

- 부트스트랩을 통해 빈 카루셀을 만들어준다.

```html
<script>
  const imgList = document.querySelector('#id_images')
  imgList.addEventListener('change',function(event){

    
    console.log(event.target.files)
    var cnt = 1
    for(var file of event.target.files){
      const maindiv = document.querySelector('.carousel-inner')
      if (cnt == 1){
        const innerDiv = document.createElement('div')
        innerDiv.classList.add('carousel-item','active')
        const innerImg = document.createElement('img')
        innerImg.width='300'
        console.log(innerImg)
        var reader = new FileReader()
        reader.onload = (function(aImg){
          return function(event){
            aImg.src = event.target.result
          }
        })(innerImg)
        reader.readAsDataURL(file)
        innerDiv.appendChild(innerImg)
        maindiv.appendChild(innerDiv)
      } else{
        const innerDiv = document.createElement('div')
        innerDiv.classList.add('carousel-item')
        const innerImg = document.createElement('img')
        innerImg.width='300'
        var reader = new FileReader()
        reader.onload = (function(aImg){
          return function(event){
            aImg.src = event.target.result
          }
        })(innerImg)
        reader.readAsDataURL(file)
        innerDiv.appendChild(innerImg)
        maindiv.appendChild(innerDiv)
      }
      cnt++
    }
  })
</script>
```

- FIleReader라는 객체를 이용하여, 사용자가 올린 img를 src에 넣어준다.
- 이렇게 하는 이유는 사용자가 올린 이미지경로와, 우리가 form에서 받아들인 이미지 경로가 다르기 때문이다.
- reader라는 변수에 FileReader라는 객체를 만들어주고, 거기에 reader.onload라고 파일을 읽었을때 실행하는 것이다.
- 뒤에 `(innerImg)`는 즉시실행함수를 이용해 aImg에 innerImg라는 변수를 넣어준것이다.
- 그리고 reader.readAsDataURL을 이용해, 사용자가 올린 파일을 base64  인코딩을 하여, URL을 만들어주고, 그걸 src에 넣어주면 된다.
- 참고 사이트 : https://www.zerocho.com/category/HTML&DOM/post/592827558653d6001804a0a5
- 참고 사이트 : https://programmingsummaries.tistory.com/367





##### 3.2.4 Post에 더 추가할 기능

-  예쁘께 css 꾸미기
- Tag를 저장하는 메소드가 없다. 그 부분을 추가할 것이다.
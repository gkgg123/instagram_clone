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


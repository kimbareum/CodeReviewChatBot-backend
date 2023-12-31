# CodeReviewChatBot-backend

## 프로젝트 목표

OpenAI API와 연동하여서, 사용자의 코드를 리뷰해주거나 코드에 대한 피드백을 제공하고, 다른 사용자의 질문 내역을 찾아보면서, 다른 사람들의 질문과 답변에서 자신이 원하는 정보를 찾아보거나 피드백을 줄 수 있는 서비스 입니다.  
이 레포지토리에서는 유저정보, 채팅내역, 댓글에 대한 관리를 하고, OpenAI API와의 통신을 하는 백엔드 서비스를 Django를 이용해서 DRF 방식으로 구축합니다.

## 개발환경 및 개발 기간

- 개발환경  
    Django 4.2.3, python 3.11.3, openai 0.27.8, djangorestframework 3.14.0, djangorestframework-simplejwt 5.2.2, django-cors-headers 4.2.0, Pillow 10.0.0, django-cleanup 8.0.0, python-decouple 3.8

- 개발기간  
    프론트엔드와 백엔드 8일

## 배포

- [배포 URL](https://kimbareum.github.io/CodeReviewChatBot/)
- [프론트엔드](https://github.com/kimbareum/CodeReviewChatBot)

- 배포환경
    - 백엔드 : AWS Lightsail, uwsgi, nginx, certbot
    - 프론트엔드 : Github Page

## 구현된 기능

1. User의 CRUD
2. Chat의 CRUD
3. 댓글의 CRUD

## ERD 모델

![ERD모델](https://github.com/kimbareum/CodeReviewChatBot/assets/131732610/6acb623e-2093-4adc-bf78-0b98a579ecd1)

## URL

### 백엔드

| URL | 기능 |
|-----|-----|
|/user/login/|로그인|
|/user/logout/|로그아웃|
|/user/signup/|회원가입|
|/user/delete/|회원탈퇴|
|/user/password/change/|비밀번호 변경|
|/user/profile/|프로필 확인 및 수정|
|/token/refresh/|JWT 토큰 갱신|
|/chat/list/|게시글목록 및 검색|
|/chat/list/self/|자신의 게시글 목록|
|/chat/detail/<chat_id>/|채팅페이지|
|/chat/<chat_id>/update/|채팅 제목 수정 및 추가질문|
|/chat/write/|채팅 페이지 작성|
|/chat/delete/<chat_id>/|채팅 삭제|
|/chat/<chat_id>/comment/write/|댓글 작성|
|/chat/comment/delete/<comment_id>|댓글 삭제|
|/chat/comment/delete/child/<childcomment_id>|대댓글 삭제(댓글과 같은 뷰)|
|/chat/comment/update/<comment_id>|댓글 수정|
|/chat/comment/update/child/<childcomment_id>|대댓글 수정(댓글과 같은 뷰)|

### 프론트엔드

| URL | 기능 |
|-----|-----|
|/|인덱스 페이지|
|/chat/<chat_id>/|채팅 페이지|
|/profile/<user_id>/|프로필 페이지|
|/user/password/change/|비밀번호 변경 페이지|
|/user/delete/|회원삭제 페이지|
|/chat/list/|게시글목록 및 검색 페이지|
|/login/|로그인 페이지|
|/signup/|회원가입 페이지|


## 상세 기능

### 회원가입 및 로그인

https://github.com/kimbareum/CodeReviewChatBot/assets/131732610/708d8bbe-1258-46ba-b02f-c2e2a5082566

- 회원가입과 로그인 페이지입니다.
- JWT를 이용하면서, access 토큰은 프론트엔드의 메모리에, refresh 토큰은 HTTP only, Secure True 옵션의 쿠키에 저장합니다.
- 로그인 여부에 따라서 사이드바에 보여지는 리스트의 여부와 버튼의 종류가 달라집니다.

### 리스트페이지 및 리스트페이지의 업데이트

https://github.com/kimbareum/CodeReviewChatBot/assets/131732610/ea33122f-8d26-4f63-866d-10bbd40d9934

- 화면 좌측의 사이드바에서는 본인이 작성한 채팅의 리스트만 표시됩니다.
- 채팅목록을 클릭하면, 다른 유저들의 채팅도 확인할 수 있습니다.
- 로그인이 되어있지 않으면 사이드바에는 채팅 리스트가 표시되지 않지만, 채팅목록 페이지는 정상적으로 접근이 가능합니다.
- 채팅목록은 최근에 업데이트된 순으로 표시됩니다.

### 검색기능

https://github.com/kimbareum/CodeReviewChatBot/assets/131732610/1cc924e6-7cdf-4997-aa1f-9ec642daf93e

- 채팅내역 중 제목, 내용, 작성자에 대한 검색이 가능합니다.

### 페이지기능

https://github.com/kimbareum/CodeReviewChatBot/assets/131732610/9c28cf2e-5eb6-470c-9b7f-25ba34cd657a

- 페이지의 전환이 가능하고, 페이지 번호는 최대 10개까지 표시됩니다.
- next 버튼과 prev 버튼은 이전페이지나 이후페이지가 존재할때만 표시됩니다.
- next 버튼과 prev 버튼으로 10개단위의 페이지 이동이 가능하고, 남아있는 페이지가 10개 이하일 경우 제일 처음페이지와 제일 마지막 페이지로 이동합니다.

### 디테일페이지

![디테일 페이지](https://github.com/kimbareum/CodeReviewChatBot/assets/131732610/24c43ce1-703b-421d-8751-80146aab2b0a)

- 디테일페이지의 구성은 위와 같습니다.
- 사용자의 질문을 백엔드로 보낸 후, 백엔드에서 OpenAI API를 통한 응답을 받아서 저장하고 프론트엔드로 응답을 전달 한 후,  프론트엔드에서 응답을 받아서 화면에 보여주게 됩니다.
- 답변은 마크다운 형식으로 받은 후 코드블럭을 ReactMarkdown과 ReactSyntaxHighlight를 이용하여서 하이라이팅 해주었습니다.

### 질문 작성 및 추가 질문

https://github.com/kimbareum/CodeReviewChatBot/assets/131732610/ad30055d-6b00-47ef-b715-9c74def99197

- 새로운 질문을 작성하고, 추가적인 질문을 할 수 있습니다.
- 새로운 질문을 작성하면 로딩화면을 보여주고, 백엔드에서 openAI API에서 응답을 받아서 채팅 데이터를 생성하게되면, 새롭게 생성된 해당 채팅의 디테일 페이지로 이동합니다.

### 채팅 삭제

https://github.com/kimbareum/CodeReviewChatBot/assets/131732610/acbf3da1-0625-4dbc-a9e2-ebddfbca462b

- 채팅의 삭제가 가능합니다.
- 채팅의 삭제는 사이드바와 채팅의 디테일 페이지 양쪽에서 가능합니다.
- 채팅의 삭제 및 수정 버튼은 해당 페이지를 소유한 유저에게만 표시됩니다.
- 채팅의 삭제시 사이드바의 채팅목록에서도 사라집니다.

### 댓글의 작성 및 삭제

https://github.com/kimbareum/CodeReviewChatBot/assets/131732610/4ef40c7d-cc33-4cca-9faa-5761467bfd06

- 댓글의 작성 및 삭제 기능입니다.
- 댓글과 댓글에 대한 대댓글 기능을 지원합니다.
- 대댓글은 depth 1까지만 지원합니다.
- 댓글과 대댓글의 삭제 버튼은 해당 댓글을 소유한 유저에게만 표시됩니다.
- 댓글의 삭제시 대댓글이 있으면 삭제된 게시글이라고 표기되고, 대댓글이 없다면 표시되지 않습니다.

### 댓글의 수정

https://github.com/kimbareum/CodeReviewChatBot/assets/131732610/d1860e9b-0d6f-4709-9dbe-f5984bf52340

- 댓글과 대댓글의 수정 기능입니다.
- 댓글과 대댓글의 삭제 버튼은 해당 댓글을 소유한 유저에게만 표시됩니다.

### 프로필 업데이트

https://github.com/kimbareum/CodeReviewChatBot/assets/131732610/8c831c28-1e3b-4322-a48a-487cb7514c7a

- 프로필의 업데이트 기능입니다.
- 사용자의 닉네임과 프로필이미지에 대한 업데이트를 지원합니다.

### 회원정보 업데이트

| ![회원정보수정페이지](https://github.com/kimbareum/CodeReviewChatBot/assets/131732610/79bba1f9-c523-4f7d-a205-bdafaf535e42) |  |
|-----|-----|
| ![비밀번호변경](https://github.com/kimbareum/CodeReviewChatBot/assets/131732610/328934a0-5c3b-4fa9-a5f3-9508ff0a989a)| ![회원탈퇴](https://github.com/kimbareum/CodeReviewChatBot/assets/131732610/fb92f8b0-ee8b-49f0-bea6-db737267a724)|

- 비밀번호 변경 및 회원탈퇴 페이지입니다.
- 회원의 비밀번호를 받아서 인증작업을 거친 후, 해당하는 작업을 수행합니다.
- 비밀번호의 변경시에는 로그아웃되어서 다시 로그인하도록 합니다.

## 느낀점

### 1. 프론트엔드와의 상호작용

모놀리식으로 구성하면, 프론트엔드로 데이터를 어떻게 넘겨줄지에 대한 큰 고민 없이, 데이터를 템플릿에서 직접 접근하여 수정할 수 있었지만, DRF를 이용하게 되면서, 데이터를 어떻게 보내줄지, 그 데이터를 어떻게 받아서 처리할지, 그리고 데이터에 이상한 정보가 함께 전달되지는 않을지에 대한 고민이 생겼습니다.  
이를 serializer의 to_representation와 validate의 오버라이딩을 적극적으로 활용해서 필요로 하는 데이터만 필요한 형태로 직렬화하도록 구성하였고, 그 데이터를 프론트엔드에서 받아서 처리할 수 있도록 하였습니다.  
```python
def validate(self, attrs):
    title = attrs.get('title')
    content = attrs.get('content')
    
    # 제목이 없을경우 제목을 자동적으로 지정합니다.
    if not title:
        writer = self.context.get('request').user
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        attrs['title'] = f"{writer}님의 {current_time} 질문"
    # 프론트에서 처리한 content가 양식에 맞지 않거나 content 값이 없을경우 에러처리합니다.
    if content and not json.loads(content)[0].get('content'):
        raise serializers.ValidationError('질문은 필수 입력 값입니다.')

    return super().validate(attrs)


def to_representation(self, instance):
    rep = super().to_representation(instance)
    # 프론트에서 필요한 정보를 추가적으로 넣어줍니다.
    rep['updated_at'] = instance.updated_at.strftime('%Y-%m-%d %H:%M')
    rep['writer_nickname'] = instance.writer.nickname
    rep['writer_profile_image'] = instance.writer.image.url
    return rep
```
이번 프로젝트에서는 혼자서 프론트엔드와 백엔드를 둘 다 구성했지만, 실제 개발 환경에서는 프론트엔드가 필요한 데이터를 백엔드에서 정확하게 파악하고 보내줘야 하기 때문에 기획단계에서 프론트엔드와 긴밀한 협의가 필요할 것 같다는 예상이 듭니다.

### 2. JWT 인증

프론트엔드와 백엔드를 분리하면서, JWT를 사용하게 되었습니다. 토큰을 관리하는데는 다양한 방법이 있었고, 그 방법들에 대해서 다양한 고민들을 해보았습니다.  
그 결과 access 토큰은 JavaScript의 메모리에 보관하고, refresh 토큰은 HTTP only, Secure True 옵션의 쿠키를 이용해서 전달하는 것이 보안과 사용자 편의성이 제일 괜찮을 것 같다는 생각이 들어서 이런 방향으로 진행했습니다.  
단순히 모든 토큰을 메모리에 저장하는 방법도 있었지만, 이 경우 새로고침을 하게되면 로그아웃이 되어버리기 때문에 편의성 측면에서 access 토큰만 메모리에 저장하기로 결정했습니다.   
이 방향으로 진행할 시, refresh 토큰이 혹시나 탈취당하더라도, SOP 때문에 access 토큰을 확인할 수 없고, access 토큰은 메모리 상에 저장되기 때문에, 탈취하기가 힘들것이라고 생각됩니다.  
로그아웃은 refresh 토큰을 블랙리스트에 추가하고, 프론트엔드에 있는 access 토큰과 refresh 토큰을 초기화하는 형태로 진행해서 확실한 로그아웃 처리를 목표료 했습니다.  

### 3. Throttle 설정

현재 사용하고 있는 OpenAI API는 사용량에 대한 요금을 지불하는 시스템이고, 기본적으로 DRF에서는 외부의 DDOS 공격이나 예상 이상의 트래픽등의 방어하는것이 필요하기 때문에, Throttle 을 적용하였습니다.   
처음에는 DRF 에서 기본적으로 지원하는 AnonRateThrottle, UserRateThrottle을 이용하려고 했지만, 이 경우 OpenAI API에 대한 Throttle을 다르게 설정하는 것이 불편했기 때문에, ScopedRateThrottle을 이용해서, 일반적인 경우와, 회원가입, OpenAI API 요청에 대한 제한을 다르게 두었습니다.  
```python
{
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': { 
        'normal': '20/minute',
        'question': '5/day',
        'signup': '1/day',  
    }
}
```

### 4. Object Manager

과거 프로젝트에서 UserObjectManager를 새로 만들었던 기억이 나서, model 차원에서 필터링이나 데이터 처리를 할 수 있을까 알아보다가, get_queryset 메서드를 오버라이딩해서, 필터처리를 할 수 있는것을 알았습니다.  
```python
class ActiveManager(models.Manager):
    
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_deleted=False)
```
이를 이용해서 논리적으로 삭제한 값들을 추가적인 필터링 없이 가져오게 하려고 했으나, Manager는 모델의 objects에 직접 접근했을때만 작동하고, prefetch_related나, select_related 등으로 참조된 값을 한번에 가져올때는 작동하지 않는것을 확인했습니다. 그래서 view에서 어떤 부분은 is_delete에 대한 처리가 없고, 어떤 경우에는 filter로 is_deleted로 가져와야하는 부분이 있었는데 이 부분이 조금 아쉽습니다.

### 5. 외부 API를 백엔드에서 이용하기

이 부분은 openAI API에서 자체적으로 제작한 패키지가 있어서, 편하게 진행했습니다.  
이 패키지의 내부구조를 살펴보니, requests 패키지를 활용하고 있는데, PyScript에서 이용해본 경험이 있으므로, 여기에서도 쉽게 적용할 수 있을 것 같습니다.

### 6. 이미지 처리

이미지를 사용하는 부분은 프로필 이미지밖에 없어서, media/profile/user_pk/경에로 uuid.*형태로 이미지를 저장하도록 pillow를 이용해서 구성해주고, 이미지가 새로 들어왔을때 django-cleanup 패키지를 이용해서, 과거 이미지가 자동 삭제되도록 설정하였습니다.

### 7. 조회수의 처리

조회수의 중복방지 알고리즘은 이전 프로젝트에서는 쿠키를 이용하였으나, 이번 프로젝트에서는 쿠키를 통해서 refresh 토큰이 전송되게 되는데, 프론트에서 cookie는 token refresh와 login 시에만 주고받도록 하고싶어서, 로컬스토리지를 이용하는 방식을 선택했습니다.  
또한 현재 페이지에 표시되는 게시글의 순서는 마지막 수정일자를 기준으로 하고 있는데, 조회수가 업데이트되면 수정일자도 업데이트 되는 현상을 발견해서, 다음과 같은 방법으로 조회수만 업데이트 되도록 바꿔주었습니다.
```python 
chat.save(update_fields=['view_count'])
```

### 8. 업데이트시 응답 데이터

현재 프론트엔드는 SPA형식으로 구성되어 있지만, 프론트엔드에서의 처리를 간편하기 하기 위해서, 어떤 요소가 업데이트될때, 전체의 정보를 보내주는 방식을 선택하고 있습니다. 이에 따라서 서비스의 규모가 커진다면, 서버측의 부담이 더 커지는 문제가 있을것으로 예상됩니다.  
앞으로도 SPA 형태의 페이지를 만들게 된다면 업데이트된 부분만 보내주고, 프론트엔드에서 그 데이터에 대해서 처리하는 방향으로 진행하는것이 더 효율적일것으로 예상됩니다.

### 9. 배포

uwsgi와 nginx를 이용한 배포작업은 이전에 진행해보았던 TechBlog 프로젝트와 크게 다르지 않았지만, 도메인을 구매하고, 도메인을 적용하고, django의 세팅을 도메인에 맞게 바꿔주고, certbot을 이용해서 https 인증서를 적용해주는 과정이 새로웠습니다. 

## 마무리하며

이번 프로젝트에서는 DRF를 이용하였는데, 많은 부분이 모놀리식 Django와는 달라지면서 다양한 고민을 하게 되었습니다.    
특히 보안측면에서 SameSite가 아니게 되면서 SOP문제가 생기는부분, JWT를 사용할때 인증에 대한 처리, Throttle에 대한 처리 등이 많이 신경쓰였습니다. 나름대로는 괜찮은 방법을 선택했다고 생각되지만, 발생할 수 있는 다른 문제들에 대해서도 잘 알아보고 싶습니다.  
또한 프론트엔드쪽 작업까지 같이 진행하면서, 데이터를 어떻게 보내주고, 어떻게 받아올지가 확실하게 정해져 있어야 성능적인 측면은 물론 편의성 측면에서도 더 좋은 결과가 나올 것 같다는 생각이 들었습니다.  
이러한 부분들을 확실하게 고려해보면서 더 다양한 프로젝트들을 진행해보고 싶습니다.
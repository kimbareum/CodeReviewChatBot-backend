# CodeReviewChatBot-backend

## 프로젝트 목표

OpenAI API와 연동하여서, 코드리뷰를 해주는 챗봇 서비스를 만들고, 사용자들이 서로가 올린 질문들을 확인하고 댓글도 달 수 있는 서비스.

## 개발환경 및 개발 기간


## 배포

- [배포 URL](https://kimbareum.github.io/CodeReviewChatBot/)
- [프론트엔드](https://github.com/kimbareum/CodeReviewChatBot)

## 구현된 기능

1. User의 CRUD

## ERD 모델


## 상세 기능

### 회원가입 및 로그인

https://github.com/kimbareum/CodeReviewChatBot/assets/131732610/708d8bbe-1258-46ba-b02f-c2e2a5082566

- 회원가입과 로그인 페이지입니다.
- JWT를 이용하여 구현하였습니다.

### 리스트페이지 및 리스트페이지의 업데이트

https://github.com/kimbareum/CodeReviewChatBot/assets/131732610/ea33122f-8d26-4f63-866d-10bbd40d9934

- 화면 좌측의 사이드바에서는 본인이 작성한 리스트만 표시됩니다.
- 채팅목록을 클릭하면, 다른 유저들의 리스트도 확인할 수 있습니다.
- 채팅목록은 최근에 업데이트된 순으로 표시됩니다.

### 검색기능

https://github.com/kimbareum/CodeReviewChatBot/assets/131732610/c534c577-af7c-41b6-8709-c01d45c3a062

- 제목, 내용, 작성자에 대한 검색이 가능합니다.

### 페이지기능

https://github.com/kimbareum/CodeReviewChatBot/assets/131732610/9c28cf2e-5eb6-470c-9b7f-25ba34cd657a

- 페이지의 전환이 가능하고, 페이지 번호는 최대 10개까지 표시됩니다.
- next 버튼과 prev 버튼으로 10개단위의 페이지 이동이 가능하고, 남아있는 페이지가 10개 이하일 경우 제일 처음페이지와 제일 마지막 페이지로 이동합니다.

### 디테일페이지

![디테일 페이지](https://github.com/kimbareum/CodeReviewChatBot/assets/131732610/24c43ce1-703b-421d-8751-80146aab2b0a)

- 디테일페이지의 구성은 위와 같습니다.
- 답변에는 코드블럭을 ReactMarckdown과 React SyntaxHighlighter를 이용하여서 하이라이팅 해주었습니다.

### 질문 작성 및 추가 질문

https://github.com/kimbareum/CodeReviewChatBot/assets/131732610/ad30055d-6b00-47ef-b715-9c74def99197

- 새로운 질문을 작성하고, 추가적인 질문을 할 수 있습니다.
- 새로운 질문을 작성하면 로딩화면을 보여주고, 작성이 완료되면 해당 디테일 페이지로 이동합니다.

### 채팅 삭제

https://github.com/kimbareum/CodeReviewChatBot/assets/131732610/acbf3da1-0625-4dbc-a9e2-ebddfbca462b

- 채팅의 삭제가 가능합니다.
- 채팅의 삭제시 사이드바의 채팅목록에서도 사라집니다.

### 댓글의 작성 및 삭제

https://github.com/kimbareum/CodeReviewChatBot/assets/131732610/4ef40c7d-cc33-4cca-9faa-5761467bfd06

- 댓글의 작성 및 삭제 기능입니다.
- 대댓글은 depth 1까지만 지원합니다.
- 댓글의 삭제시 대댓글이 있으면 삭제된 게시글이라고 표기되고, 대댓글이 없다면 표시되지 않습니다.

### 댓글의 수정

https://github.com/kimbareum/CodeReviewChatBot/assets/131732610/d1860e9b-0d6f-4709-9dbe-f5984bf52340

- 댓글의 수정 기능입니다.

### 프로필 업데이트

https://github.com/kimbareum/CodeReviewChatBot/assets/131732610/8c831c28-1e3b-4322-a48a-487cb7514c7a

- 프로필의 업데이트 기능입니다.


## 느낀점

### 1. 프론트엔드와의 상호작용

모놀리식으로 구성하면, 프론트엔드로 데이터를 어떻게 넘겨줄지에 대한 큰 고민 없이, 데이터를 템플릿에서 직접 접근하여 수정할 수 있었지만, DRF를 이용하게 되면서, 데이터를 어떻게 보내줄지, 그 데이터를 어떻게 받아서 처리할지, 그리고 데이터에 이상한 정보가 함께 전달되지는 않을지에 대한 고민이 생겼습니다.  
이를 serializer의 to_representation와 validate의 오버라이딩을 적극적으로 활용해서 필요로 하는 데이터만 필요한 형태로 직렬화하도록 구성하였고, 그 데이터를 프론트엔드에서 받아서 처리할 수 있도록 하였습니다.  
이번 프로젝트에서는 혼자서 프론트엔드와 백엔드를 둘 다 구성했지만, 실제 개발 환경에서는 프론트엔드가 필요한 데이터를 백엔드에서 정확하게 파악하고 보내줘야 하기 때문에 기획단계에서 프론트엔드와 긴밀한 협의가 필요할 것 같다는 예상이 듭니다.

### 2. JWT 인증

프론트엔드와 백엔드를 분리하면서, JWT를 사용하게 되었습니다. 토큰을 관리하는데는 다양한 방법이 있었고, 그 방법들에 대해서 다양한 고민들을 해보았습니다.  
그 결과 access 토큰은 JavaScript의 메모리에 보관하고, refresh 토큰은 HTTP only, Secure True 옵션을 이용해서 전달하는 것이 보안과 사용자 편의성이 제일 괜찮을 것 같다는 생각이 들어서 이런 방향으로 진행했습니다.  
단순히 모든 토큰을 메모리에 저장하는 방법도 있었지만, 이 경우 새로고침을 하게되면 로그아웃이 되어버리기 때문에 편의성 측면에서 access 토큰만 메모리에 저장하기로 결정했습니다.   
이 방향으로 진행할 시, refresh 토큰이 혹시나 탈취당하더라도, SOP 때문에 access 토큰을 확인할 수 없고, access 토큰은 메모리 상에 저장되기 때문에, 탈취하기가 힘들것이라고 생각됩니다.  
CSRF 토큰의 경우에는 프론트엔드와 백엔드가 분리되어 있기 때문에 사용을 하는것 자체가 복잡하고, access 토큰을 발급하는 과정에서 CORS 체크를 하기 때문에, 당장은 제거해도 괜찮을것이라고 생각했습니다.

### 3. Throttle 설정

현재 사용하고 있는 OpenAI API는 사용량에 대한 요금을 지불하는 시스템이고, 기본적으로 DRF에서는 외부의 DDOS 공격이나 예상 이상의 트래픽등의 방어하는것이 필요하기 때문에, Throttle 을 적용하였습니다.  
처음에는 DRF 에서 기본적으로 지원하는 AnonRateThrottle, UserRateThrottle을 이용하려고 했지만, 이 경우 OpenAI API에 대한 Throttle을 다르게 설정하는 것이 불편했기 때문에, ScopedRateThrottle을 이용해서, 일반적인 경우와, 회원가입, OpenAI API 요청에 대한 제한을 다르게 두었습니다.

### 4. Object Manager

과거 프로젝트에서 UserObjectManager를 새로 만들었던 기억이 나서, model 차원에서 필터링이나 데이터 처리를 할 수 있을까 알아보다가, get_queryset 메서드를 오버라이딩해서, 필터처리를 할 수 있는것을 알았습니다.  
이를 이용해서 논리적으로 삭제한 값들을 추가적인 필터링 없이 가져오게 하려고 했으나, Manager는 모델의 objects에 직접 접근했을때만 작동하고, prefetch_related나, select_related 등으로 참조된 값을 한번에 가져올때는 작동하지 않는것을 확인했습니다. 그래서 view에서 어떤 부분은 is_delete에 대한 처리가 없고, 어떤 경우에는 filter로 is_deleted로 가져와야하는 부분이 있었는데 이 부분이 조금 아쉽습니다.

### 5. 외부 API를 백엔드에서 이용하기

이 부분은 openAI API에서 자체적으로 제작한 패키지가 있어서, 편하게 진행했습니다.  
이 패키지의 내부구조를 살펴보니, requests 패키지를 활용해서 

## 하고있는일

1. ~~로딩바 만들기~~

2. ~~모달창 만들기 취소...?~~

3. ~~에러페이지 다듬기~~

4. ~~도메인 문제 해결하기~~

5. ~~페이지네이터 이전버튼, 이후버튼, 범위관리 만들기~~

6. ~~게시글 삭제 및 수정기능 구현. => delete시 chatlist도 변화하게 지정.~~

7. ~~chatGPT 연동.~~

8. ~~댓글 serializer, 대댓글 댓글 동시에 지원하게 구현해보기.~~

9. ~~푸터위치.~~

10. ~~이미지 업로드하면 과거 이미지는 삭제되게하기.~~

11. ~~CSS 파일 정리하기~~

12. ~~댓글 수정기능.~~

13. ~~배포이전에 setting에 CORS ORIGIN, ALLOW HOST 수정, 프론트엔드 API 주소 수정해야함. DEBUG 도 false로~~

14. ~~커스텀 throttle 설정이 필요할것같음.~~

15. ~~childComment 컴포넌트 분리.~~

16. ~~props들 명시화~~

17. ~~검색기능.~~

18. ~~조회수.~~ v
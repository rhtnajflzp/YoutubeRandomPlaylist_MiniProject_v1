# YoutubeRandomPlayList (Mini Project 1 - Group 24)

</br>

## 🤷 프로젝트 소개 
 <p> 입력한 키워드와 관련있는 영상을 랜덤하게 플레이 할 수 있는 사이트입니다. </p>
 <p> 키워드를 저장해 쉽게 불러와 랜덤 재생 할 수 있으며, 추가로 자신이 재미있게 본 크리에이터의 재생목록을 등록 할 수 있습니다.</p>
 <p> 또한, 다른 사람들이 등록한 플레이리스트를 자유롭게 보고 팔로우하여 언제든 볼 수 있습니다. </p>
  
  Web Site : http://youtuberandomplayer.shop/
</br>


## 🎥 시연 영상
 https://youtu.be/L1hqNuSWO0Y


## 🧑🏼‍💻 팀원 
탁예준(팀장), 김용빈,  백정수
</br>


## 🖥 개발기간

기간: 2021.11.01 ~ 2021.11.05 (5일)  
</br>


## 🏷 API Table
|기능|Method|URL|Request|Response|
|:---:|:----:|----|----|----|
|랜덤 태그</br>목록 조회|GET|/index| |{'tags' : tag}|
|Randomplaylist</br>페이지 정보 조회|GET|/randomplaylist|{'playlistid_receive': platlistId,  'author_receive': author}|{'playlistId': playlistId, 'toptags': toptags,  'likes': likes,  'like_cnt': likes_cnt,  'comments': comments,  'islike': islike}|
|Feed 페이지</br>정보 조회|GET|/feed|<user_info>|{'tags': tags,  'my_playlists': my_playlists,  'like_playlists': like_playlists,  'other_playlists': other_playlists}|
|로그인|POST|/sign_in|{'id_give': id,  'password_give': password}|{'result': result,  'token': token,  'msg': msg}|
|회원가입|POST|/sign_up/save|{'id_give': id,  'password_give': password,  'nickname_give': nickname}|{'result': result}|
|ID 중복검사|POST|/sign_up/check_dup|{'id_give': id}|{'result': result,  'exists': exists}|
|닉네임 중복검사|POST|/sign_up/check_dup2|{'nickname_give': nickname}|{'result': result,  'exists': exists}|
|영상 검색</br>결과 조회|GET|/search|{'q': query}|{'list': search_result}|
|재생목록</br>유효성 검사|POST|/playlist/search|{'plalistId_give': playlistId,  'author_give': author}|{'playlist': playlist,  'nickname': author}|
|재생목록 추가|POST|/playlist/insert|{'playlistId_give': playlistId,  'title_give': title}|{'msg': msg}|
|태그 추가|POST|/tag/insert|{'tag_give': tag}|{'msg': msg}|
|태그 삭제|POST|/tag/delete|{'tag_give': tag}|{'msg': msg}|
|태그 인기순으로</br>출력|GET|/tag_popular| |{'tags': msg}|
|댓글 작성|POST|/comment/insert|{'comment_give': comment,  'playlistId_give': playlistId,  'author_give': author}|{'msg': msg}|
|댓글 삭제|POST|/comment/delete|{'comment_give': comment,  'playlistId_give': playlistId,  'author_give': author}|{'msg': msg}|
|좋아요 추가/삭제|POST|/likelist|{'author_give': author,  'playlistId_give': playlistId}|{'msg': msg}|




</br>

## 🔨사용한 기술 스택
<code> Front-end </code>
 * JQuery
 * Bulma
 * HTML
 * CSS
 * Javascript
 
<code> Back-end </code>
 * Python 
 * Flask 
 * Jinja2
 * JWT
 * MongoDB 
 * AWS EC2
 * Google Youtube Data API V3


<code> tool </code>
 * Git
 * Figma
 * Zeplin

</br>


## ✌🏻 개인 역할

<code>탁예준</code> 전체 Page Design, CSS 

<code>김용빈</code> 전체 플레이리스트, 검색기능, 댓글, 재생목록, 좋아요 

<code>백정수</code> 로그인, 약관동의, 회원가입

</br>


## 📣 소감

<code>탁예준</code> 

<code>김용빈</code> 해결할 수 없는 문제는 스트레스지만, 해결할 수 있는 문제는 즐거움이라는 것을 느낄 수 있었습니다.

<code>백정수</code> <p> 좋은 팀장님, 팀원님을 만나 많이 성장 할 수 있었던 첫 미니프로젝트였습니다. </p>
<p>코딩적으로도 많이 배웠고 팀프로젝트에 대한 방향성, 교감 등을 나눌 수 있는 시간이 되어 큰 자산으로 남을 것 같습니다. </p>


## 📝 후기

<code>탁예준</code> 

<code>김용빈</code> https://dazbee.tistory.com/5?category=1033430

<code>백정수</code>  https://rural-coach-cc5.notion.site/99-4-1st-Project-RandomPlaylist-0ddc28f866b9460d99df84291c55a95b


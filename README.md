# YoutubeRandomPlayList (Mini Project 1)

</br>

## 🤷 Project Overview 프로젝트 소개 
 <p> Have you ever thought that there are too many options for you to chose and you just want to move to a different channel? </p>
 <p> You can insert the keyword that you are interested in and play randomly.입력한 키워드와 관련있는 영상을 랜덤하게 플레이 할 수 있는 사이트입니다. </p>
 <p> You can save your keyword channel, as well as add your favorite creators' playist. 키워드를 저장해 쉽게 불러와 랜덤 재생 할 수 있으며, 추가로 자신이 재미있게 본 크리에이터의 재생목록을 등록 할 수 있습니다.</p>
 <p> Furthermore, you can see other people's playlist and follow them. 또한, 다른 사람들이 등록한 플레이리스트를 자유롭게 보고 팔로우하여 언제든 볼 수 있습니다. </p>
  
  Web Site : http://youtuberandomplayer.shop/
</br>


## 🎥 Demo 시연 영상
 https://youtu.be/L1hqNuSWO0Y


## 🧑🏼‍💻 Team members 팀원 
Yejun Tak (Team Leader) 탁예준(팀장), Youngbin Kim 김용빈,  Jungsoo Baek 백정수
</br>


## 🖥 Developing Time 개발기간

Date 기간: 2021.11.01 ~ 2021.11.05 (5days)(5일)  
</br>


## 🏷 API Table
|Function|Method|URL|Request|Response|
|:---:|:----:|----|----|----|
|Random Tag</br>Search for the list|GET|/index| |{'tags' : tag}|
|Randomplaylist</br> Search for page information |GET|/randomplaylist|{'playlistid_receive': platlistId,  'author_receive': author}|{'playlistId': playlistId, 'toptags': toptags,  'likes': likes,  'like_cnt': likes_cnt,  'comments': comments,  'islike': islike}|
|Feed </br>search for the information|GET|/feed|<user_info>|{'tags': tags,  'my_playlists': my_playlists,  'like_playlists': like_playlists,  'other_playlists': other_playlists}|
|Login|POST|/sign_in|{'id_give': id,  'password_give': password}|{'result': result,  'token': token,  'msg': msg}|
|Register|POST|/sign_up/save|{'id_give': id,  'password_give': password,  'nickname_give': nickname}|{'result': result}|
|Duplicated ID check|POST|/sign_up/check_dup|{'id_give': id}|{'result': result,  'exists': exists}|
|Duplicated nickname check|POST|/sign_up/check_dup2|{'nickname_give': nickname}|{'result': result,  'exists': exists}|
|Search Video</br>Search result|GET|/search|{'q': query}|{'list': search_result}|
|Playlist</br>Search for Existance|POST|/playlist/search|{'plalistId_give': playlistId,  'author_give': author}|{'playlist': playlist,  'nickname': author}|
|Add Playist|POST|/playlist/insert|{'playlistId_give': playlistId,  'title_give': title}|{'msg': msg}|
|Add Tag|POST|/tag/insert|{'tag_give': tag}|{'msg': msg}|
|Delete Tag|POST|/tag/delete|{'tag_give': tag}|{'msg': msg}|
|Sort Tag by Popularity </br>export|GET|/tag_popular| |{'tags': msg}|
|Write comments |POST|/comment/insert|{'comment_give': comment,  'playlistId_give': playlistId,  'author_give': author}|{'msg': msg}|
|Delete comments|POST|/comment/delete|{'comment_give': comment,  'playlistId_give': playlistId,  'author_give': author}|{'msg': msg}|
|Add/delete likes|POST|/likelist|{'author_give': author,  'playlistId_give': playlistId}|{'msg': msg}|




</br>

## 🔨Technology Stack 사용한 기술 스택
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


## ✌🏻 Role 개인 역할

<code>탁예준</code> Front-End, Full Page Design, CSS 

<code>김용빈</code> Back-end, Searching system, Commenting system, Comments, Playist, Like 

<code>백정수</code> Log-in Page, Agreement Page, Registering Page 로그인, 약관동의, 회원가입

</br>


## 📣 Comment 소감

<code>탁예준</code> I am glad to meet an amazing team and I hope to do this sprint regularly.  

<code>김용빈</code> Indeed, unsolvable problems are stressful, but just like the puzzle, I felt joyful when I solved them. 해결할 수 없는 문제는 스트레스지만, 해결할 수 있는 문제는 즐거움이라는 것을 느낄 수 있었습니다.

<code>백정수</code> <p> I am glad to meet the amazing team leader and team-mates because of them I learned a lot of skills. 좋은 팀장님, 팀원님을 만나 많이 성장 할 수 있었던 첫 미니프로젝트였습니다. </p>
<p>As a perspective of a developer, I learned a lot as well as, how collaboration works, strong communications, I believe this experience will be a great asset of my life. 코딩적으로도 많이 배웠고 팀프로젝트에 대한 방향성, 교감 등을 나눌 수 있는 시간이 되어 큰 자산으로 남을 것 같습니다. </p>


## 📝 Blog 후기

<code>탁예준</code> None

<code>김용빈</code> https://dazbee.tistory.com/5?category=1033430

<code>백정수</code>  https://rural-coach-cc5.notion.site/99-4-1st-Project-RandomPlaylist-0ddc28f866b9460d99df84291c55a95b


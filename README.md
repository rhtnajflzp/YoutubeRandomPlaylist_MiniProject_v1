# YoutubeRandomPlayList (Mini Project 1)

</br>

## π€· Project Overview νλ‘μ νΈ μκ° 
 <p> Have you ever thought that there are too many options for you to chose and you just want to move to a different channel? </p>
 <p> You can insert the keyword that you are interested in and play randomly.</p>
 <p>μλ ₯ν ν€μλμ κ΄λ ¨μλ μμμ λλ€νκ² νλ μ΄ ν  μ μλ μ¬μ΄νΈμλλ€. </p>
 <p> You can save your keyword channel, as well as add your favorite creators' playist.</p>
 <P>ν€μλλ₯Ό μ μ₯ν΄ μ½κ² λΆλ¬μ λλ€ μ¬μ ν  μ μμΌλ©°, μΆκ°λ‘ μμ μ΄ μ¬λ―Έμκ² λ³Έ ν¬λ¦¬μμ΄ν°μ μ¬μλͺ©λ‘μ λ±λ‘ ν  μ μμ΅λλ€.</p>
 <p> Furthermore, you can see other people's playlist and follow them. </p>
  <p>λν, λ€λ₯Έ μ¬λλ€μ΄ λ±λ‘ν νλ μ΄λ¦¬μ€νΈλ₯Ό μμ λ‘­κ² λ³΄κ³  νλ‘μ°νμ¬ μΈμ λ  λ³Ό μ μμ΅λλ€. </p>
  
  Web Site : http://youtuberandomplayer.shop/
</br>


## π₯ Demo μμ° μμ
 https://youtu.be/L1hqNuSWO0Y


## π§πΌβπ» Team members νμ 
Yejun Tak (Team Leader) νμμ€(νμ₯), Youngbin Kim κΉμ©λΉ,  Jungsoo Baek λ°±μ μ
</br>


## π₯ Developing Time κ°λ°κΈ°κ°

Date κΈ°κ°: 2021.11.01 ~ 2021.11.05 (5days)(5μΌ)  
</br>


## π· API Table
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

## π¨Technology Stack μ¬μ©ν κΈ°μ  μ€ν
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


## βπ» Role κ°μΈ μ­ν 

<code>νμμ€</code> Front-End, Full Page Design, CSS 

<code>κΉμ©λΉ</code> Back-end, Searching system, Commenting system, Comments, Playist, Like 

<code>λ°±μ μ</code> Log-in Page, Agreement Page, Registering Page λ‘κ·ΈμΈ, μ½κ΄λμ, νμκ°μ

</br>


## π£ Comment μκ°

<code>νμμ€</code> I am glad to meet an amazing team and I hope to do this sprint regularly.  

<code>κΉμ©λΉ</code> Indeed, unsolvable problems are stressful, but just like the puzzle, I felt joyful when I solved them. ν΄κ²°ν  μ μλ λ¬Έμ λ μ€νΈλ μ€μ§λ§, ν΄κ²°ν  μ μλ λ¬Έμ λ μ¦κ±°μμ΄λΌλ κ²μ λλ μ μμμ΅λλ€.

<code>λ°±μ μ</code> <p> I am glad to meet the amazing team leader and team-mates because of them I learned a lot of skills. μ’μ νμ₯λ, νμλμ λ§λ λ§μ΄ μ±μ₯ ν  μ μμλ μ²« λ―Έλνλ‘μ νΈμμ΅λλ€. </p>
<p>As a perspective of a developer, I learned a lot as well as, how collaboration works, strong communications, I believe this experience will be a great asset of my life. μ½λ©μ μΌλ‘λ λ§μ΄ λ°°μ κ³  ννλ‘μ νΈμ λν λ°©ν₯μ±, κ΅κ° λ±μ λλ μ μλ μκ°μ΄ λμ΄ ν° μμ°μΌλ‘ λ¨μ κ² κ°μ΅λλ€. </p>


## π Blog νκΈ°

<code>νμμ€</code> None

<code>κΉμ©λΉ</code> https://dazbee.tistory.com/5?category=1033430

<code>λ°±μ μ</code>  https://rural-coach-cc5.notion.site/99-4-1st-Project-RandomPlaylist-0ddc28f866b9460d99df84291c55a95b


from bson.json_util import dumps
from googleapiclient.discovery import build
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime, timedelta
import random
import jwt
import hashlib

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

client = MongoClient('mongodb://test:test@localhost', 27017)
# client = MongoClient('localhost', 27017)
db = client.youtuberandomplaylist

api_key = 'Your key'
youtube = build('youtube', 'v3', developerKey=api_key)


# user token 받아오기
def get_user_info():
    token_receive = request.cookies.get('mytoken')
    # render_params의 자료형은 list로 구성.
    render_params = {}
    try:
        #유효한 token일 경우 return_params에는 user_info를 삽입해준 뒤 return
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"id": payload["id"]})
        render_params = user_info
    except jwt.ExpiredSignatureError:
        render_params['msg'] = '로그인 시간이 만료되었습니다.'
    except jwt.exceptions.DecodeError:
        render_params['msg'] = '로그인 정보가 존재하지 않습니다..'
    finally:
        return render_params


# HTML을 주는 부분
@app.route('/')
def home():
    # 서치바 아래에 표시해 줄 태그 목록 출력
    top_tags = list(db.tag.find({}, {'_id': False}).distinct('tag'))
    # 태그 목록 섞기
    random.shuffle(top_tags)
    # 받아온 태그 목록 중 3개만 출력
    top_tags_response = top_tags[:3]

    user_info = get_user_info()
    return render_template('index.html',
                           toptags=top_tags_response,
                           **user_info)


@app.route('/index')
def index():
    top_tags = list(db.tag.find({}, {'_id': False}).distinct('tag'))
    random.shuffle(top_tags)
    top_tags_response = top_tags[:3]

    user_info = get_user_info()
    return render_template('index.html',
                           toptags=top_tags_response,
                           **user_info)


@app.route('/login')
def login():
    user_info = get_user_info()
    return render_template('login.html', **user_info)


@app.route('/agreement', methods=['GET'])
def agreement():
    user_info = get_user_info()
    return render_template('agreement.html', **user_info)


@app.route('/sign_up', methods=['GET'])
def sign():
    user_info = get_user_info()
    return render_template('sign_up.html', **user_info)


@app.route('/randomplaylist', methods=['GET'])
def play():
    # 무작위 태그 목록을 5개 출력
    top_tags = list(db.tag.find({}, {'_id': False}).distinct('tag'))
    random.shuffle(top_tags)
    top_tags_response = top_tags[:5]

    # parameter 수령
    playlistId_receive = request.args.get('playlistId')
    author_receive = request.args.get('author')

    # 좋아요 목록 3개까지 가져오고 나머지는 숫자로만 받아오기
    like_cnt = 3
    likes = list(db.like_playlist.find({'author': author_receive, 'playlistId': playlistId_receive}, {'_id': False}))
    likes_response = likes[:like_cnt]
    likes_cnt = len(likes) - like_cnt

    # 댓글 목록
    comments = list(db.comment.find({'author': author_receive, 'playlistId': playlistId_receive}, {'_id': False}))

    user_info = get_user_info()
    # user_info에 'id'가 없는 경우 = 예외가 발생함 = 리스트에 'msg'밖에 없음 = 유효하지 않은 계정 
    if 'id' not in user_info:
        # islike : 좋아요를 눌렀는지 여부 판단. True일 경우 채운하트, False일 경우 빈하트로 표시해주기 위한 용도.
        # 계정이 유효하지 않을 경우에는 빈하트로 표시. 생각해보니 if 밖으로 빼도 될 것 같다. 
        islike = False
    else:
        # 좋아요 여부 체크를 위해 좋아요 컬렉션에 쿼리 진행
        likes2 = list(db.like_playlist.find({'id': user_info['id'], 'playlistId': playlistId_receive}, {'_id': False}))

        # likes2에 뭔가 들어있따 = 좋아요 한 상태다. 채운하트 비어있다 = 좋아요 안 한 상태다. 빈하트
        if likes2:
            islike = True
        else:
            islike = False

    return render_template("randomplaylist.html",
                           playlistId=playlistId_receive,
                           toptags=top_tags_response,
                           likes=likes_response,
                           likes_cnt=likes_cnt,
                           comments=comments,
                           islike=islike,
                           **user_info)


@app.route('/feed')
def feed():
    # feed창은 로그인해야만 볼 수 있음. 유효성 체크
    user_info = get_user_info()
    if 'id' not in user_info:
        # 유효하지 않은 계정일 시, 초기화면으로 이동.
        return render_template('index.html')

    # 내가 추가한 태그 목록을 출력
    tags = list(db.tag.find({'id': user_info['id']}, {'_id': False}))
    random.shuffle(tags)

    # 내가 만든 플레이리스트 목록을 출력
    my_playlists = list(db.user_playlist.find({'id': user_info['id']}, {'_id': False}))

    # 내가 좋아요 한 플레이리스트 목록을 출력
    like_playlists = list(db.like_playlist.find({'id': user_info['id']}, {'_id': False}))

    # 다른 사람들이 만든 플레이리스트 목록을 출력
    other_playlists = list(db.user_playlist.find({'id': {'$nin': [user_info['id']]}}, {'_id': False}))

    return render_template('feed.html',
                           tags=tags,
                           my_playlists=my_playlists,
                           like_playlists=like_playlists,
                           other_playlists=other_playlists,
                           **user_info)


@app.route('/modal')
def modal():
    return render_template('modal.html')


@app.route('/header')
def header():
    user_info = get_user_info()
    return render_template('header.html', **user_info)


# API 역할을 하는 부분
# login.html
@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    id_receive = request.form['id_give']
    password_receive = request.form['password_give']

    # password 데이터 암호화
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    # db를 탐색해 유저 정보가 존재하는지 확인
    result = db.users.find_one({'id': id_receive, 'password': pw_hash})

    # 유저 정보가 존재할 경우
    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }

        ##### 중요한 점 #####
        # .decode() 함수가 str 자료형에는 존재하지 않고, byte 자료형에는 있음.
        # 이유는 모르겠으나, .encode() 함수의 반환 자료형이 로컬에서는 str이고 ubuntu 환경에서는 byte임.
        # 로컬에서 같이 사용하고싶을경우 자료형을 체크해서 뒤에 .decode('utf-8')을 붙여줄 것인지 판단해야함
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# 회원가입처리
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    # 파라미터 수령
    id_receive = request.form['id_give']
    password_receive = request.form['password_give']
    nickname_receive = request.form['nickname_give']

    # 받아온 비밀번호 파라미터 암호화
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    doc = {
        "id": id_receive,  # 아이디
        "password": password_hash,  # 비밀번호
        "nickname": nickname_receive,  # 닉네임
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


# ID 중복 검사
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    id_receive = request.form['id_give']
    # db 찾아서 값이 존재하면 이미 있는 ID = 중복
    exists = bool(db.users.find_one({"id": id_receive}))
    return jsonify({'result': 'success', 'exists': exists})


# 닉네임 중복 검사
@app.route('/sign_up/check_dup2', methods=['POST'])
def check_dup2():
    nickname_receive = request.form['nickname_give']
    # db 찾아서 값이 존재하면 이미 있는 닉네임 = 중복
    exists = bool(db.users.find_one({"nickname": nickname_receive}))
    return jsonify({'result': 'success', 'exists': exists})


# randomplaylist.html
@app.route('/search', methods=['GET'])
def listing():
    # GET 타입의 파라미터 수령.
    query_receive = request.args.get('q')

    # 키워드 검색 결과 받아오기 ( Youtube Data Api 사용 )
    # q : query
    # order : 정렬 기준.
    # # date – 업로드 날짜순
    # # rating – 영상 평가순
    # # relevance – 연관 동영상으로 출력. 기본값.
    # # title – 제목 기준 오름차순.
    # # videoCount – 업로드한 동영상 개수 순.
    # # viewCount – 조회순.
    # part : 가져올 데이터. id는 안 써봐서 잘 모르겠고, snippet은 영상의 상세정보들이 전부 들어옴.
    # maxResults : 가져올 데이터의 개수. API 할당량을 고려하여 잘 설정하는것이 중요함.
    search_response = youtube.search().list(
        q=query_receive,
        order="viewCount",
        part="snippet",
        maxResults=10
    ).execute()

    return jsonify({'list': search_response})


@app.route('/playlist/search', methods=['POST'])
def search_playlist():
    playlistId_receive = request.form['playlistId_give']
    author_receive = request.form['author_give']

    # 재생목록이 실제로 등록이 되었는지 검사.
    playlist = db.user_playlist.find_one({'id': author_receive, 'playlistId': playlistId_receive})

    if playlist is not None:
        author_info = db.users.find_one({'id': author_receive},
                                        {'nickname': True})
        msg = playlist
    else:
        msg = '존재하지 않는 플레이리스트입니다.'

    # jsonify에는 list형이 들어갈 수 없어서 JSON 형태의 문자열로 변환하여 전달. response에서 다시 한 번 JSON.parse() 해줘야 사용 가능.
    return jsonify({'playlist': dumps(msg), 'nickname': dumps(author_info)})


# modal.html
@app.route('/playlist/insert', methods=['POST'])
def insert_playlist():
    user_info = get_user_info()
    if 'id' not in user_info:
        return jsonify({'msg': "유효하지 않은 회원입니다."})

    playlistId_receive = request.form['playlistId_give']
    title_receive = request.form['title_give']

    # 1. 이미 등록한 플레이리스트인지 확인
    playlist = db.user_playlist.find_one({'playlistId': playlistId_receive, 'id': user_info['id']})

    # 2. 유효한 playlistId인지 확인(Youtube Data Api 사용)
    search_response = youtube.playlists().list(
        id=playlistId_receive,
        part="snippet"
    ).execute()

    if search_response is not None:
        # 쿼리 결과를 통해 썸네일의 url을 받아오기.
        thumbnail = search_response['items'][0]['snippet']['thumbnails']['high']['url']
        if playlist is None:
            doc = {'id': user_info['id'],
                   'title': title_receive,
                   'playlistId': playlistId_receive,
                   'thumbnail': thumbnail}
            db.user_playlist.insert_one(doc)
            msg = '작성 완료!'
        else:
            msg = '작성 실패! 이미 등록한 재생목록입니다.'
    else:
        msg = '작성 실패! 잘못된 재생목록입니다.'

    return jsonify({'msg': msg})


@app.route('/tag', methods=['GET'])
def tag_show():
    id = 'test'
    tag = list(db.tag.find({'id': id}, {'_id': False}))

    return jsonify({'tags': tag})


@app.route('/tag/insert', methods=['POST'])
def tag_insert():
    user_info = get_user_info()
    if 'id' not in user_info:
        return jsonify({'msg': "유효하지 않은 회원입니다."})

    tag_receive = request.form['tag_give']

    # 유효한 태그인지 검사
    list = db.tag.find_one({'id': user_info['id'], 'tag': tag_receive})
    if list:
        msg = '이미 추가한 태그입니다.'
    else:
        doc = {
            'id': user_info['id'],
            'tag': tag_receive
        }
        db.tag.insert_one(doc)
        msg = '추가 완료!'

    return jsonify({'msg': msg})


@app.route('/tag/delete', methods=['POST'])
def tag_delete():
    user_info = get_user_info()
    if 'id' not in user_info:
        return jsonify({'msg': "유효하지 않은 회원입니다."})

    tag_receive = request.form['tag_give']
    db.tag.delete_one({'id': user_info['id'], 'tag': tag_receive})
    return jsonify({'msg': '삭제 완료!'})


@app.route('/tag/popular', methods=['GET'])
def tag_popular():
    lists = db.tag.aggregate([
        {"$group": {"_id": {"tag": "$tag", "status": "$status"}, "count": {"$sum": 1}}},
        {"$sort": {"_id.source": -1}}
    ])

    tag = []
    for list in lists:
        tag.append(list)

    return jsonify({'tags': tag})


@app.route('/tag/user_list', methods=['GET'])
def tag_user():
    tag_receive = request.args.get('tag_give')
    tag = list(db.tag.find({'tag': tag_receive}, {'_id': False}))

    return jsonify({'tags': tag})


@app.route('/tag/what_tag', methods=['GET'])
def what_tag():
    videoId_receive = request.args.get('videoId_give')
    tag = db.tag.distinct('tag', {'videoId': videoId_receive})

    return tag


@app.route('/comment/insert', methods=['POST'])
def comment_insert():
    user_info = get_user_info()
    if 'id' not in user_info:
        return jsonify({'msg': "유효하지 않은 회원입니다."})

    comment_receive = request.form['comment_give']
    playlistId_receive = request.form['playlistId_give']
    author_receive = request.form['author_give']

    db.comment.insert_one({'id': user_info['id'],
                           'nickname': user_info['nickname'],
                           'comment': comment_receive,
                           'playlistId': playlistId_receive,
                           'author': author_receive})

    return jsonify({'msg': '작성 완료!'})


@app.route('/comment/delete', methods=['POST'])
def comment_delete():
    id_receive = request.form['id_give']
    comment_receive = request.form['comment_give']
    videoId_receive = request.form['videoId_give']

    db.comment.delete_one({'id': id_receive,
                           'comment': comment_receive,
                           'videoId': videoId_receive})

    return jsonify({'msg': '삭제 완료!'})


@app.route('/user/playlist', methods=['GET'])
def user_playlist():
    id_receive = request.args.get('id_give')
    playlistId = list(db.user_playlist.find({'id': id_receive}, {'_id': False}))
    return jsonify({'playlist': playlistId})


@app.route('/likelist', methods=['POST'])
def user_like():
    user_info = get_user_info()
    if 'id' not in user_info:
        return jsonify({'msg': "유효하지 않은 회원입니다."})

    author_receive = request.form['author_give']
    playlistId_receive = request.form['playlistId_give']
    print(author_receive, playlistId_receive)
    like_playlist = db.like_playlist.find_one({'id': user_info['id'],
                                               'author': author_receive,
                                               'playlistId': playlistId_receive})

    thumbnail = db.user_playlist.find_one({'id': author_receive, 'playlistId': playlistId_receive},
                                          {'thumbnail': True})

    doc = {'id': user_info['id'],
           'author': author_receive,
           'playlistId': playlistId_receive,
           'thumbnail': thumbnail['thumbnail']}

    if like_playlist is None:
        db.like_playlist.insert_one(doc)
        msg = '작성 완료!'
    else:
        db.like_playlist.delete_one(doc)
        msg = '삭제 완료!'

    return jsonify({'msg': msg})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

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

client = MongoClient('localhost', 27017)
db = client.youtuberandomplaylist

api_key = 'AIzaSyDoc0GN-_nBuANpy8f893HDttg71tF5szs'
youtube = build('youtube', 'v3', developerKey=api_key)


def get_user_info():
    token_receive = request.cookies.get('mytoken')
    render_params = {}
    try:
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
    # 가장 많이 추가한 상위 3개의 태그 목록만 출력
    top_tags = list(db.tag.find({}, {'_id': False}).distinct('tag'))
    random.shuffle(top_tags)
    top_tags_response = top_tags[:3]

    user_info = get_user_info()
    return render_template('index.html',
                           toptags=top_tags_response,
                           **user_info)


@app.route('/index')
def index():
    # 가장 많이 추가한 상위 3개의 태그 목록만 출력
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

    playlistId_receive = request.args.get('playlistId')
    author_receive = request.args.get('author')

    # 플레이리스트
    likes = list(db.like_playlist.find({'playlistId': playlistId_receive}, {'_id': False}))
    likes_response = likes[:2]
    likes_cnt = len(likes) - 2

    # 댓글 목록
    comments = list(db.comment.find({'author': author_receive, 'playlistId': playlistId_receive}, {'_id': False}))

    user_info = get_user_info()

    return render_template("randomplaylist.html",
                           playlistId=playlistId_receive,
                           toptags=top_tags_response,
                           likes=likes_response,
                           likes_cnt=likes_cnt,
                           comments=comments,
                           **user_info)


@app.route('/feed')
def feed():
    user_info = get_user_info()
    if 'id' not in user_info:
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

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'id': id_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    id_receive = request.form['id_give']
    password_receive = request.form['password_give']
    nickname_receive = request.form['nickname_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "id": id_receive,  # 아이디
        "password": password_hash,  # 비밀번호
        "nickname": nickname_receive,  # 닉네임
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    id_receive = request.form['id_give']
    exists = bool(db.users.find_one({"id": id_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/sign_up/check_dup2', methods=['POST'])
def check_dup2():
    nickname_receive = request.form['nickname_give']
    exists = bool(db.users.find_one({"nickname": nickname_receive}))
    return jsonify({'result': 'success', 'exists': exists})


#randomplaylist.html
@app.route('/search', methods=['GET'])
def listing():
    query_receive = request.args.get('q')

    # 키워드 검색 결과 받아오기 ( Youtube Data Api 사용 )
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
    playlist = db.user_playlist.find_one({'id': author_receive, 'playlistId': playlistId_receive})

    if playlist is not None:
        author_info = db.users.find_one({'id': author_receive},
                                        {'nickname': True})
        msg = playlist
    else:
        msg = '존재하지 않는 플레이리스트입니다.'

    return jsonify({'playlist': dumps(msg), 'nickname': dumps(author_info)})


#modal.html
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

    thumbnail = ''

    msg = 'Hi!'

    if search_response is not None:
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

    doc = {
        'id': user_info['id'],
        'tag': tag_receive
    }

    db.tag.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})


@app.route('/tag/delete', methods=['POST'])
def tag_delete():
    id_receive = request.form['id_give']
    tag_receive = request.form['tag_give']
    db.tag.delete_one({'id': id_receive, 'tag': tag_receive})
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


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


@app.route('/user/playlist', methods=['GET'])
def user_playlist():
    id_receive = request.args.get('id_give')
    playlistId = list(db.user_playlist.find({'id': id_receive}, {'_id': False}))
    return jsonify({'playlist': playlistId})


@app.route('/user/likelist', methods=['GET'])
def user_likelist():
    id_receive = request.form['id_give']
    likelistId = list(db.like_playlist.find({'id': id_receive}, {'_id': False}))
    return jsonify({'playlist': likelistId})


@app.route('/user/like', methods=['POST'])
def user_like():
    id_receive = request.form['id_give']  # 클라이언트에서 좋아요 와 작성자의 정보를 POST에 넘겨 줌
    author_receive = request.form['author_give']
    likelistId_receive = request.form['likelistId_give']  # 좋아요를 눌렀는지 판단??

    like_playlist = db.like_playlist.find_one({'id': id_receive, 'author': author_receive})

    like_response = youtube.playlists().list(
        id=likelistId_receive,
        part="snippet"
    ).execute()

    thumbnail = ''

    if like_response is not None:
        thumbnail = like_response['items'][0]['snippet']['thumbnails']['high']['url']

        if like_playlist is None:
            doc = {'id': id_receive,
                   'author': author_receive,
                   'likelistId': likelistId_receive,
                   'thumbnail': thumbnail}
            db.user_playlist.insert_one(doc)
            msg = '작성 완료!'
        else:
            msg = '작성 실패! 이미 등록한 재생목록입니다.'
    else:
        msg = '작성 실패! 잘못된 재생목록입니다.'

    return jsonify({'msg': msg})
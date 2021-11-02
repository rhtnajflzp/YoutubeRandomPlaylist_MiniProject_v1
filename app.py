from googleapiclient.discovery import build
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbteamproj

api_key = 'AIzaSyDoc0GN-_nBuANpy8f893HDttg71tF5szs'
youtube = build('youtube', 'v3', developerKey=api_key)


# HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/play')
def play():
    return render_template("play.html")


@app.route('/mypage')
def mypage():
    return render_template("mypage.html")


# API 역할을 하는 부분
@app.route('/search', methods=['GET'])
def listing():
    query_receive = request.args.get('q')

    # 키워드 검색 결과 받아오기
    search_response = youtube.search().list(
        q=query_receive,
        order="date",
        part="snippet",
        maxResults=50
    ).execute()

    return jsonify({'list': search_response})


@app.route('/search', methods=['POST'])
def saving():
    return jsonify({'msg': '저장이 완료되었습니다!'})


@app.route('/tag', methods=['GET'])
def tag_show():
    id = 'test'
    tag = list(db.tag.find({'id': id}, {'_id': False}))

    return jsonify({'tags': tag})


@app.route('/tag/insert', methods=['POST'])
def tag_insert():
    id_receive = request.form['id_give']
    tag_receive = request.form['tag_give']
    videoId_receive = request.form['videoId_give']

    doc = {
        'id': id_receive,
        'tag': tag_receive,
        'videoId': videoId_receive
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


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

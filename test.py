from googleapiclient.discovery import build
from flask import Flask, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient
from werkzeug.utils import secure_filename
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

doc = {'id':'test', 'playlistId':'PLguPqKADXoCEw_vJqW0VSNTKejjUAk2wY'}
db.followlist.insert_one(doc)
doc = {'id':'love', 'playlistId':'PLguPqKADXoCEw_vJqW0VSNTKejjUAk2wY'}
db.followlist.insert_one(doc)
doc = {'id':'tasty', 'playlistId':'PLguPqKADXoCEw_vJqW0VSNTKejjUAk2wY'}
db.followlist.insert_one(doc)
doc = {'id':'beauty', 'playlistId':'PLguPqKADXoCEw_vJqW0VSNTKejjUAk2wY'}
db.followlist.insert_one(doc)
doc = {'id':'king', 'playlistId':'PLguPqKADXoCEw_vJqW0VSNTKejjUAk2wY'}
db.followlist.insert_one(doc)
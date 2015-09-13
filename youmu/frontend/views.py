__author__ = 'badpoet'

import os 

from flask import (Flask, Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort,send_from_directory)

from werkzeug import secure_filename, SharedDataMiddleware
from youmu.config import DefaultConfig

frontend = Blueprint("frontend", __name__)

# simple demo of foundation 5
@frontend.route('/foundation')
def foundation():
    return render_template('foundation-index.html')

@frontend.route('/', methods=['GET'])
def index():
    query = request.args.get("query", "")
    return render_template('index.html', query=query)
    # return render_template('index.html')

@frontend.route('/demo')
def demo():
    return render_template('demo.html')

@frontend.route('/videos/<video_id>')
def display(video_id):
    return render_template('video.html', video_id = video_id)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in DefaultConfig.ALLOWED_EXTENSIONS

@frontend.route('/upload', methods=['GET', 'POST'])
def to_upload_file():
    print DefaultConfig.UPLOAD_FOLDER
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(DefaultConfig.UPLOAD_FOLDER + filename)
            #return redirect(url_for('index'))
    return render_template('upload.html')

@frontend.route('/player')
def player():
    return render_template('player.html')

@frontend.route('/user/')
def to_my_area():
    return render_template('user/index.html')

@frontend.route('/live/')
def live():
    return render_template('live.html')


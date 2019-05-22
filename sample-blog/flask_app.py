import sqlite3, json, random, string

from functools import wraps
from datetime import timedelta
from threading import Timer
from werkzeug.utils import secure_filename

from flask import Flask, make_response, g, request, send_from_directory
from flask import render_template, url_for, redirect, flash, jsonify
from flask import session as user_session

import flask_app_queries



# --- Setup --- #

app = Flask(__name__)

def login_required(f):
    ''' Checks If User Is Logged In '''
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'session_id' in user_session:
            return f(*args, **kwargs)
        else:
            # flash('Please Log In To Use This Site.')
            return redirect('/signin')

    return decorated_function


def ajax_login_required(f):
    ''' Checks If User Is Logged In '''
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'session_id' in user_session:
            return f(*args, **kwargs)
        else:
            return jsonify(error = True, message = 'Not signed in')

    return decorated_function


@app.route('/', methods=['GET'])
def welcome():
  logged_in = True if 'session_id' in user_session else False
  return render_template('welcome.html', logged_in = logged_in)

@app.route('/users/<string:username>', methods=['GET'])
def user_page_by_username(username):
  logged_in = True if 'session_id' in user_session else False
  return render_template('user-page.html', logged_in = logged_in)

@app.route('/users/<int:user_id>', methods=['GET'])
def user_page_by_id(user_id):
  logged_in = True if 'session_id' in user_session else False
  return render_template('user-page.html', logged_in = logged_in)

@app.route('/posts/<int:post_id>', methods=['GET'])
def post_page(post_id):
  logged_in = True if 'session_id' in user_session else False
  return render_template('post-page.html', logged_in = logged_in)




# ajax routes #

@app.route('/get_latest_posts', methods=['GET'])
def get_latest_posts():
  posts = flask_app_queries.get_latest_posts()
  return jsonify(posts = posts)

@app.route('/get_latest_posts/<int:post_id>', methods=['GET'])
def get_latest_posts_post_id(post_id):
  posts = flask_app_queries.get_latest_posts(post_id)
  return jsonify(posts = posts)

@app.route('/get_post_by_id/<int:post_id>', methods=['GET'])
def get_post_by_id(post_id):
  post = flask_app_queries.get_post_by_id(post_id)
  return jsonify(post = post)

@app.route('/get_user_by_id/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
  user = flask_app_queries.get_user_by_id(user_id)
  return jsonify(user = user)

@app.route('/get_user_by_username/<string:username>', methods=['GET'])
def get_user_by_username(username):
  user = flask_app_queries.get_user_by_username(username)
  return jsonify(user = user)


# --- Listen --- #

if __name__ == "__main__":
  app.secret_key = 'DF6Y#6G15$)F&*DFj/Y4DR'
  app.debug = True
  app.run( host = '0.0.0.0' , port = 7000 )
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
app.secret_key = 'DF6Y#6G15$)F&*DFj/Y4DR'

def uniqueValue():
  value = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(50))
  return value.lower()

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
  you_id = user_session['you_id'] if 'you_id' in user_session else False
  return render_template('welcome.html', logged_in = logged_in, you_id = you_id)

@app.route('/tags', methods=['GET'])
def tags_page():
  logged_in = True if 'session_id' in user_session else False
  you_id = user_session['you_id'] if 'you_id' in user_session else False
  return render_template('tags-page.html', logged_in = logged_in, you_id = you_id)

@app.route('/tags/<int:tag_id>', methods=['GET'])
def posts_by_tag_page(tag_id):
  logged_in = True if 'session_id' in user_session else False
  you_id = user_session['you_id'] if 'you_id' in user_session else False
  return render_template('posts-by-tag.html', logged_in = logged_in, you_id = you_id)

@app.route('/login', methods=['GET'])
def login_page():
  if 'session_id' in user_session:
    return redirect('/')
  return render_template('login-page.html')

@app.route('/signup', methods=['GET'])
def signup_page():
  if 'session_id' in user_session:
    return redirect('/')
  return render_template('signup-page.html')

@app.route('/signout', methods=['GET'])
def signout():
  user_session.clear()
  return redirect('/')

@app.route('/notifications', methods=['GET'])
def notifications_page():
  logged_in = True if 'session_id' in user_session else False
  you_id = user_session['you_id'] if 'you_id' in user_session else False
  if 'session_id' not in user_session:
    return redirect('/')
  return render_template('notifications-page.html', logged_in = logged_in, you_id = you_id)

@app.route('/messages', methods=['GET'])
def messages_page():
  logged_in = True if 'session_id' in user_session else False
  you_id = user_session['you_id'] if 'you_id' in user_session else False
  if 'session_id' not in user_session:
    return redirect('/')
  return render_template('messages-page.html', logged_in = logged_in, you_id = you_id)





# @app.route('/users/<string:username>', methods=['GET'])
# def user_page_by_username(username):
#   logged_in = True if 'session_id' in user_session else False
#   return render_template('user-page.html', logged_in = logged_in)

@app.route('/users/<int:user_id>', methods=['GET'])
def user_page_by_id(user_id):
  # user = flask_app_queries.get_user_by_id(user_id)
  # if not user:
  #   return redirect('/')

  logged_in = True if 'session_id' in user_session else False
  you_id = user_session['you_id'] if 'you_id' in user_session else False
  return render_template('user-page.html', logged_in = logged_in, you_id = you_id)

@app.route('/posts/<int:post_id>', methods=['GET'])
def post_page_by_id(post_id):
  logged_in = True if 'session_id' in user_session else False
  you_id = user_session['you_id'] if 'you_id' in user_session else False
  return render_template('post-page.html', logged_in = logged_in, you_id = you_id)




# ajax routes #

@app.route('/check_session', methods=['GET'])
def check_session():
  if 'session_id' in user_session:
    you_id = user_session['you_id']
    user = flask_app_queries.get_user_by_id(you_id)
    return jsonify(online = True, user = user)
  else:
    return jsonify(online = False)

@app.route('/get_latest_posts', methods=['GET'])
def get_latest_posts():
  posts = flask_app_queries.get_latest_posts()
  return jsonify(posts = posts)

@app.route('/get_latest_posts/<int:post_id>', methods=['GET'])
def get_latest_posts_post_id(post_id):
  posts = flask_app_queries.get_latest_posts(post_id)
  return jsonify(posts = posts)

@app.route('/get_latest_tags', methods=['GET'])
def get_latest_tags():
  tags = flask_app_queries.get_latest_tags(tag_id = None)
  return jsonify(tags = tags)

@app.route('/get_latest_tags/<int:tag_id>', methods=['GET'])
def get_latest_tags_tag_id(tag_id):
  tags = flask_app_queries.get_latest_tags(tag_id = tag_id)
  return jsonify(tags = tags)

@app.route('/users/<int:user_id>/get_latest_posts', methods=['GET'])
def get_user_latest_posts(user_id):
  user_posts = flask_app_queries.get_user_latest_posts(user_id = user_id, post_id = None)
  return jsonify(posts = user_posts)

@app.route('/users/<int:user_id>/get_latest_posts/<int:post_id>', methods=['GET'])
def get_user_latest_posts_post_id(user_id, post_id):
  user_posts = flask_app_queries.get_user_latest_posts(user_id = user_id, post_id = post_id)
  return jsonify(posts = user_posts)


@app.route('/tags/<int:tag_id>/get_latest_posts/', methods=['GET'])
def get_tag_latest_posts(tag_id):
  tag_posts = flask_app_queries.get_tag_latest_posts(tag_id = tag_id, post_tag_id = None)
  return jsonify(posts = tag_posts)

@app.route('/tags/<int:tag_id>/get_latest_posts/<int:post_tag_id>', methods=['GET'])
def get_tag_latest_posts_post_tag_id(tag_id, post_tag_id):
  tag_posts = flask_app_queries.get_tag_latest_posts(tag_id = tag_id, post_tag_id = post_tag_id)
  return jsonify(posts = tag_posts)


@app.route('/get_post_by_id/<int:post_id>', methods=['GET'])
def get_post_by_id(post_id):
  post = flask_app_queries.get_post_by_id(post_id)
  return jsonify(post = post)

@app.route('/get_tag_by_id/<int:tag_id>', methods=['GET'])
def get_tag_by_id(tag_id):
  tag = flask_app_queries.get_tag_by_id(tag_id)
  return jsonify(tag = tag)

@app.route('/get_user_by_id/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
  user = flask_app_queries.get_user_by_id(user_id)
  return jsonify(user = user)

@app.route('/get_user_by_username/<string:username>', methods=['GET'])
def get_user_by_username(username):
  user = flask_app_queries.get_user_by_username(username)
  return jsonify(user = user)

@app.route('/posts/<int:post_id>/get_latest_comments', methods=['GET'])
def get_latest_comments(post_id):
  post_comments = flask_app_queries.get_latest_comments(post_id = post_id, comment_id = None)
  return jsonify(comments = post_comments)

@app.route('/posts/<int:post_id>/get_latest_comments/<int:comment_id>', methods=['GET'])
def get_latest_comments_comment_id(post_id, comment_id):
  post_comments = flask_app_queries.get_latest_comments(post_id = post_id, comment_id = comment_id)
  return jsonify(comments = post_comments)


@app.route('/users/<int:user_id>/get_latest_notifications', methods=['GET'])
def get_latest_notifications(user_id):
  if 'session_id' not in user_session:
    return jsonify(error = True, message = 'Not Logged In')
  you_id = user_session['you_id']
  if you_id != user_id:
    return jsonify(error = True, message = 'Not Authorized')
  user_notifications = flask_app_queries.get_latest_notifications(user_id = you_id, notification_id = None)
  return jsonify(notifications = user_notifications)

@app.route('/users/<int:user_id>/get_latest_notifications/<int:notification_id>', methods=['GET'])
def get_latest_notifications_notification_id(user_id, notification_id):
  if 'session_id' not in user_session:
    return jsonify(error = True, message = 'Not Logged In')
  you_id = user_session['you_id']
  if you_id != user_id:
    return jsonify(error = True, message = 'Not Authorized')
  user_notifications = flask_app_queries.get_latest_notifications(user_id = you_id, notification_id = notification_id)
  return jsonify(notifications = user_notifications)

@app.route('/users/<int:user_id>/get_message_senders', methods=['GET'])
def get_message_senders(user_id):
  if 'session_id' not in user_session:
    return jsonify(error = True, message = 'Not Logged In')
  you_id = user_session['you_id']
  if you_id != user_id:
    return jsonify(error = True, message = 'Not Authorized')
  message_senders = flask_app_queries.get_message_senders(user_id = you_id, message_id = None)
  return jsonify(senders = message_senders)

@app.route('/users/<int:user_id>/get_message_senders/<int:message_id>', methods=['GET'])
def get_message_senders_message_id(user_id, message_id):
  if 'session_id' not in user_session:
    return jsonify(error = True, message = 'Not Logged In')
  you_id = user_session['you_id']
  if you_id != user_id:
    return jsonify(error = True, message = 'Not Authorized')
  message_senders = flask_app_queries.get_message_senders(user_id = you_id, message_id = message_id)
  return jsonify(senders = message_senders)

@app.route('/users/<int:user_id>/sender/<int:sender_id>/get_latest_messages', methods=['GET'])
def get_messages_by_sender(user_id, sender_id):
  if 'session_id' not in user_session:
    return jsonify(error = True, message = 'Not Logged In')
  you_id = user_session['you_id']
  if you_id != user_id:
    return jsonify(error = True, message = 'Not Authorized')
  messages = flask_app_queries.get_messages_by_sender(user_id = you_id, sender_id = sender_id, message_id = None)
  return jsonify(messages = messages)

@app.route('/users/<int:user_id>/sender/<int:sender_id>/get_latest_messages/<int:message_id>', methods=['GET'])
def get_messages_by_sender_message_id(user_id, sender_id, message_id):
  if 'session_id' not in user_session:
    return jsonify(error = True, message = 'Not Logged In')
  you_id = user_session['you_id']
  if you_id != user_id:
    return jsonify(error = True, message = 'Not Authorized')
  messages = flask_app_queries.get_messages_by_sender(user_id = you_id, sender_id = sender_id, message_id = message_id)
  return jsonify(messages = messages)




@app.route('/log_in', methods=['PUT'])
def login_route():
  data = json.loads(request.data) if request.data else None
  if not data:
    return jsonify(error = True, message = "request data not provided")

  if "email" not in data:
    return jsonify(error = True, message = "Email Address field is required")

  if "pswrd" not in data:
    return jsonify(error = True, message = "Password field is required")

  you = flask_app_queries.login(data)

  if you:
    user_session['session_id'] = uniqueValue()
    user_session['you_id'] = you['id']
    return jsonify(message = 'logged in successfully', user = you)
  else:
    return jsonify(message = 'invalid credentials', error = True)



# --- Listen --- #

if __name__ == "__main__":
  app.debug = True
  app.run( host = '0.0.0.0' , port = 7000 )
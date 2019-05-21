import sqlite3, uuid
import lorem
import random, string, sys, os, datetime

from namegenerator import generate_word

sql_file = 'schema2.sql'
db_file = 'blog.db'
init_data_sql = 'init-data.sql'
epoch = datetime.datetime.utcfromtimestamp(0)



if os.path.exists(init_data_sql):
  os.remove(init_data_sql)

init_data_sql_file = open(init_data_sql, "w+")


def uniqueValue():
  value = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(50))
  return value.lower()

def unix_time_millis(dt):
  return (dt - epoch).total_seconds() * 1000.0

def create_tables(delete_db = False):
  try:
    if delete_db == True:
      if os.path.exists(db_file):
        print('deleting db...')
        os.remove(db_file)
        print('deleted db succesfully')

    commands_list = ''
    with open(sql_file) as fp:
      commands_list = fp.read().split(';')[:-1]

    conn = sqlite3.connect(db_file)

    for command in commands_list:
      try:
        conn.execute(command)
        conn.commit()
      except Exception as e:
        print('command failed...')
        print(command)
        raise e
    conn.close()
    print('tables created successfully')
  except Exception as e:
    print('error: could not create tables...')
    print(e)
  

user_ids = []
tag_ids = []
post_ids = []
comment_ids = []

action_types = {
  'follow': 'follow',
  'new_post': 'new_post',
  'post_like': 'post_like',
  'new_comment': 'new_comment',
  'comment_like': 'comment_like',
  'new_message': 'new_message',
}

target_types = {
  'follow': 'follow',
  'post': 'post',
  'post_like': 'post_like',
  'comment': 'comment',
  'comment_like': 'comment_like',
  'message': 'message',
}

notifications_latest_id = 1



def create_users():
  conn = sqlite3.connect(db_file)

  for user_id in range(1, 1001):
    try:
      user_ids.append(user_id)

      displayname = generate_word(12)
      username = str(user_id) + '-' + generate_word(15)
      email = generate_word(17) + '@' + generate_word(5) + '.com'
      pswrd = str(unix_time_millis(datetime.datetime.today())) + uniqueValue()
      bio = lorem.sentence()
      UUID = uuid.uuid1()
      date_created = str(datetime.datetime.today())

      command = '''
      INSERT INTO users (id, displayname, username, email, pswrd, bio, uuid, date_created)
      VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s')
      ''' % (user_id, displayname, username, email, pswrd, bio, UUID, date_created)

      conn.execute(command)
      conn.commit()

      init_data_sql_file.write(command)

    except Exception as e:
      print('failed...')
      print(e)
      print(command)
      break

  conn.close()
  print('created users successfully')

def create_follows():
  conn = sqlite3.connect(db_file)

  for followings_id in range(1, 9001):
    try:
      user1_id = 0
      user2_id = 0
      while user1_id == user2_id:
        user1_id = random.choice(user_ids)
        user2_id = random.choice(user_ids)

      UUID = uuid.uuid1()
      date_created = str(datetime.datetime.today())

      command = '''
      INSERT INTO followings (id, user_id, follows_id, uuid, date_created)
      VALUES (%s, %s, %s, '%s', '%s')
      ''' % (followings_id, user1_id, user2_id, UUID, date_created)

      conn.execute(command)
      conn.commit()

      init_data_sql_file.write(command)

      create_notification(
        conn = conn,
        from_id = user1_id,
        user_id = user2_id,
        action_type = action_types['follow'],
        target_type = target_types['follow'],
        target_id = followings_id,
        link = ''
      )

    except Exception as e:
      print('failed...')
      print(e)
      print(command)
      break

  conn.close()
  print('created followings successfully')

def create_tags():
  conn = sqlite3.connect(db_file)

  for tag_id in range(1, 2501):
    try:
      tag_ids.append(tag_id)
      tag_name = generate_word(7)

      command = '''
      INSERT INTO tags (id, name)
      VALUES (%s, '%s')
      ''' % (tag_id, tag_name)

      conn.execute(command)
      conn.commit()

      init_data_sql_file.write(command)

    except Exception as e:
      print('failed...')
      print(e)
      print(command)
      break

  conn.close()
  print('created tags successfully')
  
def create_posts():
  conn = sqlite3.connect(db_file)

  for post_id in range(1, 10001):
    try:
      post_ids.append(post_id)

      owner_id = random.choice(user_ids)
      title = lorem.sentence()
      body = lorem.paragraph() + lorem.paragraph()
      UUID = uuid.uuid1()
      date_created = str(datetime.datetime.today())

      command = '''
      INSERT INTO posts (id, owner_id, title, body, uuid, date_created)
      VALUES (%s, %s, '%s', '%s', '%s', '%s')
      ''' % (post_id, owner_id, title, body, UUID, date_created)

      conn.execute(command)
      conn.commit()

      init_data_sql_file.write(command)

    except Exception as e:
      print('failed...')
      print(e)
      print(command)
      break

  conn.close()
  print('created posts successfully')

def create_comments():
  conn = sqlite3.connect(db_file)

  for comment_id in range(1, 50001):
    try:
      comment_ids.append(comment_id)

      owner_id = random.choice(user_ids)
      post_id = random.choice(post_ids)
      body = lorem.paragraph()
      UUID = uuid.uuid1()
      date_created = str(datetime.datetime.today())

      command = '''
      INSERT INTO comments (id, owner_id, post_id, body, uuid, date_created)
      VALUES (%s, %s, %s, '%s', '%s', '%s')
      ''' % (comment_id, owner_id, post_id, body, UUID, date_created)

      conn.execute(command)
      conn.commit()

      init_data_sql_file.write(command)

      cur = conn.execute('SELECT owner_id FROM posts WHERE id = %s' % (post_id,))
      row = cur.fetchone()

      create_notification(
        conn = conn,
        from_id = owner_id,
        user_id = row[0],
        action_type = action_types['new_comment'],
        target_type = target_types['comment'],
        target_id = comment_id,
        link = ''
      )

    except Exception as e:
      print('failed...')
      print(e)
      print(command)
      break

  conn.close()
  print('created comments successfully')

def create_post_likes():
  conn = sqlite3.connect(db_file)

  for post_like_id in range(1, 10001):
    try:
      user_id = random.choice(user_ids)
      post_id = random.choice(post_ids)
      UUID = uuid.uuid1()
      date_created = str(datetime.datetime.today())

      command = '''
      INSERT INTO post_likes (id, user_id, post_id, uuid, date_created)
      VALUES (%s, %s, %s, '%s', '%s')
      ''' % (post_like_id, user_id, post_id, UUID, date_created)

      conn.execute(command)
      conn.commit()

      cur = conn.execute('SELECT owner_id FROM posts WHERE id = %s' % (post_id,))
      row = cur.fetchone()

      init_data_sql_file.write(command)

      create_notification(
        conn = conn,
        from_id = user_id,
        user_id = row[0],
        action_type = action_types['post_like'],
        target_type = target_types['post'],
        target_id = post_id,
        link = ''
      )

    except Exception as e:
      print('failed...')
      print(e)
      print(command)
      break

  conn.close()
  print('created post likes successfully')

def create_comment_likes():
  conn = sqlite3.connect(db_file)

  for comment_like_id in range(1, 6001):
    try:
      user_id = random.choice(user_ids)
      comment_id = random.choice(comment_ids)
      UUID = uuid.uuid1()
      date_created = str(datetime.datetime.today())

      command = '''
      INSERT INTO comment_likes (id, user_id, comment_id, uuid, date_created)
      VALUES (%s, %s, %s, '%s', '%s')
      ''' % (comment_like_id, user_id, comment_id, UUID, date_created)

      conn.execute(command)
      conn.commit()

      cur = conn.execute('SELECT owner_id FROM comments WHERE id = %s' % (comment_id,))
      row = cur.fetchone()

      init_data_sql_file.write(command)

      create_notification(
        conn = conn,
        from_id = user_id,
        user_id = row[0],
        action_type = action_types['comment_like'],
        target_type = target_types['comment'],
        target_id = comment_id,
        link = ''
      )

    except Exception as e:
      print('failed...')
      print(e)
      print(command)
      break

  conn.close()
  print('created comment likes successfully')

def create_post_tags():
  conn = sqlite3.connect(db_file)

  for post_tag_id in range(1, 4001):
    try:
      post_id = random.choice(post_ids)
      tag_id = random.choice(tag_ids)

      command = '''
      INSERT INTO post_tags (id, post_id, tag_id)
      VALUES (%s, %s, %s)
      ''' % (post_tag_id, post_id, tag_id)

      conn.execute(command)
      conn.commit()

    except Exception as e:
      print('failed...')
      print(e)
      print(command)
      break

  conn.close()
  print('created post tags successfully')

def create_comment_tags():
  conn = sqlite3.connect(db_file)

  for comment_tag_id in range(1, 2001):
    try:
      comment_id = random.choice(comment_ids)
      tag_id = random.choice(tag_ids)

      command = '''
      INSERT INTO comment_tags (id, comment_id, tag_id)
      VALUES (%s, %s, %s)
      ''' % (comment_tag_id, comment_id, tag_id)

      conn.execute(command)
      conn.commit()

    except Exception as e:
      print('failed...')
      print(e)
      print(command)
      break

  conn.close()
  print('created comment tags successfully')

def create_messages():
  conn = sqlite3.connect(db_file)

  for message_id in range(1, 7001):
    try:
      sender_id = 0
      recipient_id = 0
      while sender_id == recipient_id:
        sender_id = random.choice(user_ids)
        recipient_id = random.choice(user_ids)

      content = lorem.sentence()
      UUID = uuid.uuid1()
      dt = str(datetime.datetime.today())
      date_sent = dt
      date_created = dt

      command = '''
      INSERT INTO messages (id, sender_id, recipient_id, content, date_sent, uuid, date_created)
      VALUES (%s, %s, %s, '%s', '%s', '%s', '%s')
      ''' % (message_id, sender_id, recipient_id, content, date_sent, UUID, date_created)

      conn.execute(command)
      conn.commit()

      init_data_sql_file.write(command)

      create_notification(
        conn = conn,
        from_id = sender_id,
        user_id = recipient_id,
        action_type = action_types['new_message'],
        target_type = target_types['message'],
        target_id = message_id,
        link = ''
      )

    except Exception as e:
      print('failed...')
      print(e)
      print(command)
      break

  conn.close()
  print('created messages successfully')

def create_notification(conn, from_id, user_id, action_type, target_type, target_id, link = ''):
  try:
    global notifications_latest_id
    UUID = uuid.uuid1()
    date_created = str(datetime.datetime.today())

    sql_command = '''
    INSERT INTO notifications (id, from_id, user_id, action_type, target_type, target_id, link, uuid, date_created)
    VALUES (%s, %s, %s, '%s', '%s', '%s', '%s', '%s', '%s')
    ''' % (notifications_latest_id, from_id, user_id, action_type, target_type, target_id, link, UUID, date_created)

    conn.execute(sql_command)
    conn.commit()

    init_data_sql_file.write(sql_command)

  except Exception as e:
    print('failed...')
    print(e)
    print(sql_command)

  notifications_latest_id = notifications_latest_id + 1



def init():
  print('initializing...')
  create_tables(delete_db = True)

  create_users()
  create_tags()
  create_follows()
  
  create_posts()
  create_post_likes()
  create_post_tags()

  create_comments()
  create_comment_likes()
  create_comment_tags()

  create_messages()



init()
print('sample data created!')
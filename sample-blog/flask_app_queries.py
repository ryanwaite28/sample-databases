import sqlite3
from chamber import apply_notification_message

db_file = 'blog.db'



def get_latest_posts(post_id = None):
  if not post_id:
    query = '''
    SELECT posts.id AS PostID, posts.owner_id AS PostOwnerID, posts.title AS PostTitle, posts.body AS PostBody, posts.date_created AS PostDateCreated, posts.uuid AS PostUuid, 
      users.displayname AS OwnerDisplayname, users.username AS OwnerUsername, 
      users.icon_link AS OwnerIconLink, users.date_created AS OwnerDateCreated,
      (SELECT COUNT(post_likes.id) FROM post_likes WHERE post_likes.post_id = posts.id) AS PostLikesCount,
      (SELECT COUNT(comments.id) FROM comments WHERE comments.post_id = posts.id) AS CommentsCount
    FROM posts
    JOIN users ON posts.owner_id = users.id
    ORDER BY posts.id DESC
    LIMIT 5 
    '''
  else:
    query = '''
    SELECT posts.id AS PostID, posts.owner_id AS PostOwnerID, posts.title AS PostTitle, posts.body AS PostBody, posts.date_created AS PostDateCreated, posts.uuid AS PostUuid, 
      users.displayname AS OwnerDisplayname, users.username AS OwnerUsername, 
      users.icon_link AS OwnerIconLink, users.date_created AS OwnerDateCreated,
      (SELECT COUNT(post_likes.id) FROM post_likes WHERE post_likes.post_id = posts.id) AS PostLikesCount,
      (SELECT COUNT(comments.id) FROM comments WHERE comments.post_id = posts.id) AS CommentsCount
    FROM posts
    JOIN users ON posts.owner_id = users.id
    WHERE posts.id < %s
    ORDER BY posts.id DESC
    LIMIT 5 
    ''' % (post_id,)

  conn = sqlite3.connect(db_file)
  cur1 = conn.execute(query)
  posts_rows = cur1.fetchall()

  data_list = []

  for post_row in posts_rows:
    tags_list = []

    command = '''
    SELECT tags.id, tags.name
    FROM post_tags
    JOIN tags ON post_tags.tag_id = tags.id
    WHERE post_tags.post_id = %s
    LIMIT 10
    ''' % (post_row[0],)

    cur2 = conn.execute(command)
    tags_rows = cur2.fetchall()

    for r in tags_rows:
      tags_list.append({
        "id": r[0],
        "name": r[1],
      })

    data_list.append({
      "id": post_row[0],
      "owner_id": post_row[1],
      "title": post_row[2],
      "body": post_row[3],
      "date_created": post_row[4],
      "uuid": post_row[5],
      "owner": {
        "displayname": post_row[6],
        "username": post_row[7],
        "icon_link": post_row[8],
        "date_created": post_row[9],
      },
      "likes": post_row[10],
      "comments_count": post_row[11],
      "tags": tags_list,
    })

  conn.close()
  return data_list

def get_user_latest_posts(user_id, post_id):
  if not post_id:
    query = '''
    SELECT posts.id AS PostID, posts.owner_id AS PostOwnerID, 
      posts.title AS PostTitle, posts.body AS PostBody, 
      posts.date_created AS PostDateCreated, posts.uuid AS PostUuid, 
      (SELECT COUNT(post_likes.id) FROM post_likes WHERE post_likes.post_id = posts.id) AS PostLikesCount,
      (SELECT COUNT(comments.id) FROM comments WHERE comments.post_id = posts.id) AS CommentsCount
    FROM posts
    WHERE posts.owner_id = %s
    ORDER BY posts.id DESC
    LIMIT 5 
    ''' % (user_id,)
  else:
    query = '''
    SELECT posts.id AS PostID, posts.owner_id AS PostOwnerID, 
      posts.title AS PostTitle, posts.body AS PostBody, 
      posts.date_created AS PostDateCreated, posts.uuid AS PostUuid, 
      (SELECT COUNT(post_likes.id) FROM post_likes WHERE post_likes.post_id = posts.id) AS PostLikesCount,
      (SELECT COUNT(comments.id) FROM comments WHERE comments.post_id = posts.id) AS CommentsCount
    FROM posts
    WHERE posts.id < %s AND posts.owner_id = %s
    ORDER BY posts.id DESC
    LIMIT 5 
    ''' % (post_id, user_id)

  conn = sqlite3.connect(db_file)
  cur1 = conn.execute(query)
  posts_rows = cur1.fetchall()

  data_list = []

  for post_row in posts_rows:
    tags_list = []

    command = '''
    SELECT tags.id, tags.name
    FROM post_tags
    JOIN tags ON post_tags.tag_id = tags.id
    WHERE post_tags.post_id = %s
    LIMIT 10
    ''' % (post_row[0],)

    cur2 = conn.execute(command)
    tags_rows = cur2.fetchall()

    for r in tags_rows:
      tags_list.append({
        "id": r[0],
        "name": r[1],
      })

    data_list.append({
      "id": post_row[0],
      "owner_id": post_row[1],
      "title": post_row[2],
      "body": post_row[3],
      "date_created": post_row[4],
      "uuid": post_row[5],
      "likes": post_row[6],
      "comments_count": post_row[7],
      "tags": tags_list,
    })

  conn.close()
  return data_list



def get_post_by_id(post_id):
  query = '''
    SELECT posts.id AS PostID, posts.owner_id AS PostOwnerID, posts.title AS PostTitle, posts.body AS PostBody, posts.date_created AS PostDateCreated, posts.uuid AS PostUuid, 
      users.displayname AS OwnerDisplayname, users.username AS OwnerUsername, 
      users.icon_link AS OwnerIconLink, users.date_created AS OwnerDateCreated,
      (SELECT COUNT(post_likes.id) FROM post_likes WHERE post_likes.post_id = posts.id) AS PostLikesCount,
      (SELECT COUNT(comments.id) FROM comments WHERE comments.post_id = posts.id) AS CommentsCount
    FROM posts
    JOIN users ON posts.owner_id = users.id
    WHERE PostID = %s
    ORDER BY PostID DESC
    LIMIT 5 
    ''' % (post_id,)
  
  conn = sqlite3.connect(db_file)
  cur1 = conn.execute(query)
  post_row = cur1.fetchone()

  if not post_row:
    conn.close()
    return None

  tags_list = []

  command = '''
  SELECT tags.id, tags.name
  FROM post_tags
  JOIN tags ON post_tags.tag_id = tags.id
  WHERE post_tags.post_id = %s
  LIMIT 10
  ''' % (post_row[0],)

  cur2 = conn.execute(command)
  tags_rows = cur2.fetchall()

  for r in tags_rows:
    tags_list.append({
        "id": r[0],
        "name": r[1],
      })

  post = {
    "id": post_row[0],
    "owner_id": post_row[1],
    "title": post_row[2],
    "body": post_row[3],
    "date_created": post_row[4],
    "uuid": post_row[5],
    "owner": {
      "displayname": post_row[6],
      "username": post_row[7],
      "icon_link": post_row[8],
      "date_created": post_row[9],
    },
    "likes": post_row[10],
    "comments_count": post_row[11],
    "tags": tags_list,
  }

  conn.close()
  return post


def get_user_by_id(user_id):
  query = '''
    SELECT id, displayname, username, bio, icon_link, weblink, date_created
    FROM users
    WHERE id = %s
    ''' % (user_id,)
  
  conn = sqlite3.connect(db_file)
  cur1 = conn.execute(query)
  user_row = cur1.fetchone()

  if not user_row:
    conn.close()
    return None

  user = {
    "id": user_row[0],
    "displayname": user_row[1],
    "username": user_row[2],
    "bio": user_row[3],
    "icon_link": user_row[4],
    "weblink": user_row[5],
    "date_created": user_row[6],
  }

  conn.close()
  return user



def get_user_by_username(username):
  query = '''
    SELECT id, displayname, username, bio, icon_link, weblink, date_created
    FROM users
    WHERE username = '%s'
    ''' % (username,)
  
  conn = sqlite3.connect(db_file)
  cur1 = conn.execute(query)
  user_row = cur1.fetchone()

  if not user_row:
    conn.close()
    return None

  user = {
    "id": user_row[0],
    "displayname": user_row[1],
    "username": user_row[2],
    "bio": user_row[3],
    "icon_link": user_row[4],
    "weblink": user_row[5],
    "date_created": user_row[6],
  }

  conn.close()
  return user

def login(data):
  query = '''
    SELECT id, displayname, username, bio, icon_link, weblink, date_created
    FROM users
    WHERE (email = '%s' OR username = '%s') AND pswrd = '%s'
    ''' % (data['email'], data['email'], data['pswrd'])
  
  conn = sqlite3.connect(db_file)
  cur1 = conn.execute(query)
  user_row = cur1.fetchone()

  if not user_row:
    conn.close()
    return None

  user = {
    "id": user_row[0],
    "displayname": user_row[1],
    "username": user_row[2],
    "bio": user_row[3],
    "icon_link": user_row[4],
    "weblink": user_row[5],
    "date_created": user_row[6],
  }

  conn.close()
  return user

def get_latest_comments(post_id, comment_id):
  if not comment_id:
    query = '''
    SELECT comments.id AS CommentID, comments.owner_id AS CommentOwnerID, comments.post_id AS CommentPostId, comments.body AS CommentBody, comments.date_created AS CommentDateCreated, comments.uuid AS CommentUuid, 
      users.displayname AS OwnerDisplayname, users.username AS OwnerUsername, 
      users.icon_link AS OwnerIconLink, users.date_created AS OwnerDateCreated,
      (SELECT COUNT(comment_likes.id) FROM comment_likes WHERE comment_likes.comment_id = comments.id) AS CommentLikesCount
    FROM comments
    JOIN users ON comments.owner_id = users.id
    WHERE comments.post_id = %s
    ORDER BY comments.id DESC
    LIMIT 5 
    ''' % (post_id,)
  else:
    query = '''
    SELECT comments.id AS CommentID, comments.owner_id AS CommentOwnerID, comments.post_id AS CommentPostId, comments.body AS CommentBody, comments.date_created AS CommentDateCreated, comments.uuid AS CommentUuid, 
      users.displayname AS OwnerDisplayname, users.username AS OwnerUsername, 
      users.icon_link AS OwnerIconLink, users.date_created AS OwnerDateCreated,
      (SELECT COUNT(comment_likes.id) FROM comment_likes WHERE comment_likes.comment_id = comments.id) AS CommentLikesCount
    FROM comments
    JOIN users ON comments.owner_id = users.id
    WHERE comments.post_id = %s AND comments.id < %s
    ORDER BY comments.id DESC
    LIMIT 5 
    ''' % (post_id, comment_id)

  conn = sqlite3.connect(db_file)
  cur1 = conn.execute(query)
  comments_rows = cur1.fetchall()

  data_list = []

  for comment_row in comments_rows:
    tags_list = []

    command = '''
    SELECT tags.id, tags.name
    FROM comment_tags
    JOIN tags ON comment_tags.tag_id = tags.id
    WHERE comment_tags.comment_id = %s
    LIMIT 10
    ''' % (comment_row[0],)

    cur2 = conn.execute(command)
    tags_rows = cur2.fetchall()

    for r in tags_rows:
      tags_list.append({
        "id": r[0],
        "name": r[1],
      })

    data_list.append({
      "id": comment_row[0],
      "owner_id": comment_row[1],
      "post_id": comment_row[2],
      "body": comment_row[3],
      "date_created": comment_row[4],
      "uuid": comment_row[5],
      "owner": {
        "displayname": comment_row[6],
        "username": comment_row[7],
        "icon_link": comment_row[8],
        "date_created": comment_row[9],
      },
      "likes": comment_row[10],
      "tags": tags_list,
    })

  conn.close()
  return data_list

def get_latest_notifications(user_id, notification_id):
  if not notification_id:
    query = '''
    SELECT notifications.id AS NotesID, notifications.from_id AS NotesFromID, notifications.user_id AS NotesUserID,
      notifications.action_type AS NotesActionType, notifications.target_type AS NotesTargetType, 
      notifications.target_id AS NotesTargetID, notifications.link AS NotesLink,
      notifications.uuid AS NotesUuid, notifications.date_created AS NotesDateCreated,
      users.displayname AS FromDisplayname, users.username AS FromUsername, 
      users.icon_link AS FromIconLink, users.date_created AS FromDateCreated
    FROM notifications
    JOIN users ON notifications.from_id = users.id 
    WHERE notifications.user_id = %s
    ORDER BY notifications.id DESC
    LIMIT 5
    ''' % (user_id,)
  else:
    query = '''
    SELECT notifications.id AS NotesID, notifications.from_id AS NotesFromID, notifications.user_id AS NotesUserID,
      notifications.action_type AS NotesActionType, notifications.target_type AS NotesTargetType, 
      notifications.target_id AS NotesTargetID, notifications.link AS NotesLink,
      notifications.uuid AS NotesUuid, notifications.date_created AS NotesDateCreated,
      users.displayname AS FromDisplayname, users.username AS FromUsername, 
      users.icon_link AS FromIconLink, users.date_created AS FromDateCreated
    FROM notifications
    JOIN users ON notifications.from_id = users.id 
    WHERE notifications.user_id = %s AND notifications.id < %s
    ORDER BY notifications.id DESC
    LIMIT 5
    ''' % (user_id, notification_id)

  conn = sqlite3.connect(db_file)
  cur1 = conn.execute(query)
  notifications_rows = cur1.fetchall()

  data_list = []

  for notes_row in notifications_rows:
    data = {
      "id": notes_row[0],
      "from_id": notes_row[1],
      "user_id": notes_row[2],
      "action_type": notes_row[3],
      "target_type": notes_row[4],
      "target_id": notes_row[5],
      "link": notes_row[6],
      "uuid": notes_row[7],
      "date_created": notes_row[8],
      "from": {
        "id": notes_row[1],
        "displayname": notes_row[9],
        "username": notes_row[10],
        "icon_link": notes_row[11],
        "date_created": notes_row[12],
      },
    }

    apply_notification_message(data)

    data_list.append(data)

  conn.close()
  return data_list

def get_message_senders(user_id, message_id):
  if not message_id:
    query = '''
    SELECT messages.id AS MsgID, messages.sender_id AS MsgSenderID,
      users.displayname AS SenderDisplayname, users.username AS SenderUsername, 
      users.icon_link AS SenderIconLink, users.date_created AS SenderDateCreated
    FROM messages
    JOIN users ON messages.sender_id = users.id 
    WHERE messages.recipient_id = %s
    GROUP BY messages.sender_id
    ORDER BY messages.id DESC
    LIMIT 5
    ''' % (user_id,)
  else:
    query = '''
    SELECT messages.id AS MsgID, messages.sender_id AS MsgSenderID,
      users.displayname AS SenderDisplayname, users.username AS SenderUsername, 
      users.icon_link AS SenderIconLink, users.date_created AS SenderDateCreated
    FROM messages
    JOIN users ON messages.sender_id = users.id 
    WHERE messages.recipient_id = %s AND messages.id < %s
    GROUP BY messages.sender_id
    ORDER BY messages.id DESC
    LIMIT 5
    ''' % (user_id, message_id)

  conn = sqlite3.connect(db_file)
  cur1 = conn.execute(query)
  message_senders_rows = cur1.fetchall()

  data_list = []

  for row in message_senders_rows:
    data_list.append({
      "id": row[0],
      "sender_id": row[1],
      "sender": {
        "id": row[1],
        "displayname": row[2],
        "username": row[3],
        "icon_link": row[4],
        "date_created": row[5],
      }
    })

  conn.close()
  return data_list

def get_messages_by_sender(user_id, sender_id, message_id):
  if not message_id:
    query = '''
    SELECT messages.id AS MsgID, messages.sender_id AS MsgSenderID, messages.recipient_id AS MsgRecipientID,
      messages.content AS MsgContent, messages.date_sent AS MsgDateSent, messages.date_read AS MsgDateRead,
      messages.uuid AS MsgUuid, messages.date_created AS MsgDateCreated,
      users.displayname AS SenderDisplayname, users.username AS SenderUsername, 
      users.icon_link AS SenderIconLink, users.date_created AS SenderDateCreated
    FROM messages
    JOIN users ON messages.sender_id = users.id 
    WHERE ((messages.recipient_id = %s AND messages.sender_id = %s) 
	    OR (messages.recipient_id = %s AND messages.sender_id = %s))
    ORDER BY messages.id DESC
    LIMIT 5;
    ''' % (user_id, sender_id, sender_id, user_id)
  else:
    query = '''
    SELECT messages.id AS MsgID, messages.sender_id AS MsgSenderID, messages.recipient_id AS MsgRecipientID,
      messages.content AS MsgContent, messages.date_sent AS MsgDateSent, messages.date_read AS MsgDateRead,
      messages.uuid AS MsgUuid, messages.date_created AS MsgDateCreated,
      users.displayname AS SenderDisplayname, users.username AS SenderUsername, 
      users.icon_link AS SenderIconLink, users.date_created AS SenderDateCreated
    FROM messages
    JOIN users ON messages.sender_id = users.id 
    WHERE ((messages.recipient_id = %s AND messages.sender_id = %s) 
	    OR (messages.recipient_id = %s AND messages.sender_id = %s)) 
      AND messages.id < %s 
    ORDER BY messages.id DESC
    LIMIT 5;
    ''' % (user_id, sender_id, sender_id, user_id, message_id)

  conn = sqlite3.connect(db_file)
  cur1 = conn.execute(query)
  messages_rows = cur1.fetchall()

  data_list = []

  for row in messages_rows:
    data_list.append({
      "id": row[0],
      "sender_id": row[1],
      "recipient_id": row[2],
      "content": row[3],
      "date_sent": row[4],
      "date_read": row[5],
      "uuid": row[6],
      "date_created": row[7],
      "sender": {
        "id": row[1],
        "displayname": row[8],
        "username": row[9],
        "icon_link": row[10],
        "date_created": row[11],
      }
    })

  conn.close()
  return data_list


def get_latest_tags(tag_id):
  if not tag_id:
    query = '''
    SELECT tags.id, tags.name,
      (SELECT COUNT(post_tags.id) FROM post_tags WHERE post_tags.tag_id = tags.id) AS PostsByTagCount
    FROM tags
    ORDER BY tags.id DESC
    LIMIT 20
    '''
  else:
    query = '''
    SELECT tags.id, tags.name,
      (SELECT COUNT(post_tags.id) FROM post_tags WHERE post_tags.tag_id = tags.id) AS PostsByTagCount
    FROM tags
    WHERE id < %s
    ORDER BY tags.id DESC
    LIMIT 20
    ''' % (tag_id,)

  conn = sqlite3.connect(db_file)
  cur1 = conn.execute(query)
  tags_rows = cur1.fetchall()

  data_list = []

  for row in tags_rows:
    data_list.append({
      "id": row[0],
      "name": row[1],
      "posts_by_tag_count": row[2]
    })

  conn.close()
  return data_list

def get_tag_by_id(tag_id):
  if not tag_id:
    return None
  
  query = '''
  SELECT tags.id, tags.name,
    (SELECT COUNT(post_tags.id) FROM post_tags WHERE post_tags.tag_id = tags.id) AS PostsByTagCount
  FROM tags
  WHERE id = %s 
  '''  % (tag_id,)

  conn = sqlite3.connect(db_file)
  cur1 = conn.execute(query)
  tag_row = cur1.fetchone()

  if not tag_row:
    conn.close()
    return None

  tag = {
    "id": tag_row[0],
    "name": tag_row[1],
    "posts_by_tag_count": tag_row[2]
  }

  conn.close()
  return tag

def get_tag_latest_posts(tag_id, post_tag_id):
  if not post_tag_id:
    query = '''
    SELECT post_tags.id AS PostTagID, post_tags.tag_id AS TagID, tags.name AS TagName, posts.id AS PostID, posts.owner_id AS PostOwnerID, posts.title AS PostTitle, posts.body AS PostBody, posts.date_created AS PostDateCreated, posts.uuid AS PostUuid, 
      users.displayname AS OwnerDisplayname, users.username AS OwnerUsername, 
      users.icon_link AS OwnerIconLink, users.date_created AS OwnerDateCreated,
      (SELECT COUNT(post_likes.id) FROM post_likes WHERE post_likes.post_id = posts.id) AS PostLikesCount,
      (SELECT COUNT(comments.id) FROM comments WHERE comments.post_id = posts.id) AS CommentsCount
    FROM post_tags
    JOIN tags ON post_tags.tag_id = tags.id
    JOIN users ON posts.owner_id = users.id
    JOIN posts ON post_tags.post_id = posts.id
    WHERE post_tags.tag_id = %s
    ORDER BY post_tags.id DESC
    LIMIT 5
    ''' % (tag_id,)
  else:
    query = '''
    SELECT post_tags.id AS PostTagID, post_tags.tag_id AS TagID, tags.name AS TagName, posts.id AS PostID, posts.owner_id AS PostOwnerID, posts.title AS PostTitle, posts.body AS PostBody, posts.date_created AS PostDateCreated, posts.uuid AS PostUuid, 
      users.displayname AS OwnerDisplayname, users.username AS OwnerUsername, 
      users.icon_link AS OwnerIconLink, users.date_created AS OwnerDateCreated,
      (SELECT COUNT(post_likes.id) FROM post_likes WHERE post_likes.post_id = posts.id) AS PostLikesCount,
      (SELECT COUNT(comments.id) FROM comments WHERE comments.post_id = posts.id) AS CommentsCount
    FROM post_tags
    JOIN tags ON post_tags.tag_id = tags.id
    JOIN users ON posts.owner_id = users.id
    JOIN posts ON post_tags.post_id = posts.id
    WHERE post_tags.tag_id = %s AND post_tags.id < %s
    ORDER BY post_tags.id DESC
    LIMIT 5
    ''' % (tag_id, post_tag_id)

  conn = sqlite3.connect(db_file)
  cur1 = conn.execute(query)
  posts_rows = cur1.fetchall()

  data_list = []

  for post_row in posts_rows:
    tags_list = []

    command = '''
    SELECT tags.id, tags.name
    FROM post_tags
    JOIN tags ON post_tags.tag_id = tags.id
    WHERE post_tags.post_id = %s
    LIMIT 10
    ''' % (post_row[3],)

    cur2 = conn.execute(command)
    tags_rows = cur2.fetchall()

    for r in tags_rows:
      tags_list.append({
        "id": r[0],
        "name": r[1],
      })

    data_list.append({
      "id": post_row[0],
      "tag_id": post_row[1],
      "tag_name": post_row[2],
      "post_id": post_row[3],
      "post": {
        "id": post_row[3],
        "owner_id": post_row[4],
        "title": post_row[5],
        "body": post_row[6],
        "date_created": post_row[7],
        "uuid": post_row[8],
        "owner": {
          "displayname": post_row[9],
          "username": post_row[10],
          "icon_link": post_row[11],
          "date_created": post_row[12],
        },
        "likes": post_row[13],
        "comments_count": post_row[14],
        "tags": tags_list,
      }
    })

  conn.close()
  return data_list
import sqlite3

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
    SELECT tags.name AS TagName
    FROM post_tags
    JOIN tags ON post_tags.tag_id = tags.id
    WHERE post_tags.post_id = %s
    LIMIT 10
    ''' % (post_row[0],)

    cur2 = conn.execute(command)
    tags_rows = cur2.fetchall()

    for r in tags_rows:
      tags_list.append(r[0])

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
    SELECT tags.name AS TagName
    FROM post_tags
    JOIN tags ON post_tags.tag_id = tags.id
    WHERE post_tags.post_id = %s
    LIMIT 10
    ''' % (post_row[0],)

    cur2 = conn.execute(command)
    tags_rows = cur2.fetchall()

    for r in tags_rows:
      tags_list.append(r[0])

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
  SELECT tags.name AS TagName
  FROM post_tags
  JOIN tags ON post_tags.tag_id = tags.id
  WHERE post_tags.post_id = %s
  LIMIT 10
  ''' % (post_row[0],)

  cur2 = conn.execute(command)
  tags_rows = cur2.fetchall()

  for r in tags_rows:
    tags_list.append(r[0])

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
    SELECT tags.name AS TagName
    FROM comment_tags
    JOIN tags ON comment_tags.tag_id = tags.id
    WHERE comment_tags.comment_id = %s
    LIMIT 10
    ''' % (comment_row[0],)

    cur2 = conn.execute(command)
    tags_rows = cur2.fetchall()

    for r in tags_rows:
      tags_list.append(r[0])

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
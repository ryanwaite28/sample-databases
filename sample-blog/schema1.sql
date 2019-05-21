CREATE TABLE IF NOT EXISTS users (
  id int NOT NULL AUTOINCREMENT,

  displayname varchar(255) NOT NULL,
  username varchar(255) NOT NULL,
  email varchar(255) NOT NULL,
  pswrd varchar(255) NOT NULL,
  bio varchar(255),
  weblink varchar(255),
  icon_id varchar(255),
  icon_link varchar(255),
  uuid varchar(255) DEFAULT NEWID(),
  date_created datetime DEFAULT GetDate(),

  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS followings (
  id int NOT NULL AUTOINCREMENT,
  
  user_id int NOT NULL,
  follows_id int NOT NULL,
  uuid varchar(255) DEFAULT NEWID(),
  date_created datetime DEFAULT GetDate(),

  PRIMARY KEY (id),
  CONSTRAINT followings_user FOREIGN KEY follows (user_id) REFERENCES users (id),
  CONSTRAINT followings_follow FOREIGN KEY follows (follows_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS subscriptions (
  id int NOT NULL AUTOINCREMENT,
  
  user_id int NOT NULL,
  subscribes_to_id int NOT NULL,
  subscribe_content_type varchar(255) NOT NULL,
  deliver_sms boolean NOT NULL,
  deliver_email boolean NOT NULL,
  deliver_notification boolean NOT NULL,
  uuid varchar(255) DEFAULT NEWID(),
  date_created datetime DEFAULT GetDate(),

  PRIMARY KEY (id),
  CONSTRAINT subscriber_user FOREIGN KEY subscriptions (user_id) REFERENCES users (id),
  CONSTRAINT subscribee_user FOREIGN KEY subscriptions (subscribes_to_id) REFERENCES users (id)
);



CREATE TABLE IF NOT EXISTS posts (
  id int NOT NULL AUTOINCREMENT,
  
  owner_id int NOT NULL,
  title varchar(255) NOT NULL,
  body varchar(500) NOT NULL,
  uuid varchar(255) DEFAULT NEWID(),
  date_created datetime DEFAULT GetDate(),

  PRIMARY KEY (id),
  CONSTRAINT post_owner FOREIGN KEY posts (owner_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS post_likes (
  id int NOT NULL AUTOINCREMENT,
  
  user_id int NOT NULL,
  post_id int NOT NULL,
  uuid varchar(255) DEFAULT NEWID(),
  date_created datetime DEFAULT GetDate(),

  PRIMARY KEY (id),
  CONSTRAINT post_like_user FOREIGN KEY post_likes (user_id) REFERENCES users (id),
  CONSTRAINT post_like_post FOREIGN KEY post_likes (post_id) REFERENCES posts (id)
);

CREATE TABLE IF NOT EXISTS comments (
  id int NOT NULL AUTOINCREMENT,
  
  owner_id int NOT NULL,
  post_id int NOT NULL,
  title varchar(255) NOT NULL,
  body varchar(500) NOT NULL,
  uuid varchar(255) DEFAULT NEWID(),
  date_created datetime DEFAULT GetDate(),

  PRIMARY KEY (id),
  CONSTRAINT comment_owner FOREIGN KEY comments (owner_id) REFERENCES users (id),
  CONSTRAINT comment_post FOREIGN KEY comments (post_id) REFERENCES posts (id)
);

CREATE TABLE IF NOT EXISTS comment_likes (
  id int NOT NULL AUTOINCREMENT,
  
  user_id int NOT NULL,
  comment_id int NOT NULL,
  uuid varchar(255) DEFAULT NEWID(),
  date_created datetime DEFAULT GetDate(),

  PRIMARY KEY (id),
  CONSTRAINT comment_like_user FOREIGN KEY comment_likes (user_id) REFERENCES users (id),
  CONSTRAINT comment_like_comment FOREIGN KEY comment_likes (comment_id) REFERENCES comments (id)
);

CREATE TABLE IF NOT EXISTS messages (
  id int NOT NULL AUTOINCREMENT,
  
  sender_id int NOT NULL,
  recipient_id int NOT NULL,
  content varchar(255) NOT NULL,
  date_sent datetime DEFAULT GetDate(),
  date_read datetime,
  uuid varchar(255) DEFAULT NEWID(),
  date_created datetime DEFAULT GetDate(),

  PRIMARY KEY (id),
  CONSTRAINT message_sender FOREIGN KEY messages (sender_id) REFERENCES users (id),
  CONSTRAINT message_recipient FOREIGN KEY messages (recipient_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS notifications (
  id int NOT NULL AUTOINCREMENT,

  for_id int NOT NULL,
  content varchar(255) NOT NULL,
  link varchar(255),
  uuid varchar(255) DEFAULT NEWID(),
  date_created datetime DEFAULT GetDate(),

  PRIMARY KEY (id),
  CONSTRAINT notification_user FOREIGN KEY notifications (for_id) REFERENCES users (id)
);
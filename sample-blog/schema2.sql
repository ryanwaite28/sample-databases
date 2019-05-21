CREATE TABLE IF NOT EXISTS users (
  id int NOT NULL,

  displayname varchar(255) NOT NULL,
  username varchar(255) NOT NULL UNIQUE,
  email varchar(255) NOT NULL UNIQUE,
  pswrd varchar(255) NOT NULL,
  bio varchar(255),
  weblink varchar(255),
  icon_id varchar(255),
  icon_link varchar(255),
  uuid varchar(255) UNIQUE,
  date_created datetime,

  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS followings (
  id int NOT NULL,
  
  user_id int NOT NULL,
  follows_id int NOT NULL,
  uuid varchar(255) UNIQUE,
  date_created datetime,

  PRIMARY KEY (id),
  CONSTRAINT followings_user FOREIGN KEY (user_id) REFERENCES users (id),
  CONSTRAINT followings_follow FOREIGN KEY (follows_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS subscriptions (
  id int NOT NULL,
  
  user_id int NOT NULL,
  subscribes_to_id int NOT NULL,
  subscribe_content_type varchar(255) NOT NULL,
  deliver_sms boolean NOT NULL,
  deliver_email boolean NOT NULL,
  deliver_notification boolean NOT NULL,
  uuid varchar(255) UNIQUE,
  date_created datetime,

  PRIMARY KEY (id),
  CONSTRAINT subscriber_user FOREIGN KEY (user_id) REFERENCES users (id),
  CONSTRAINT subscribee_user FOREIGN KEY (subscribes_to_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS tags (
  id int NOT NULL,
  name varchar(255) NOT NULL,
  PRIMARY KEY (id)
);



CREATE TABLE IF NOT EXISTS posts (
  id int NOT NULL,
  
  owner_id int NOT NULL,
  title varchar(255) NOT NULL,
  body varchar(500) NOT NULL,
  uuid varchar(255) UNIQUE,
  date_created datetime,

  PRIMARY KEY (id),
  CONSTRAINT post_owner FOREIGN KEY (owner_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS post_likes (
  id int NOT NULL,
  
  user_id int NOT NULL,
  post_id int NOT NULL,
  uuid varchar(255) UNIQUE,
  date_created datetime,

  PRIMARY KEY (id),
  CONSTRAINT post_like_user FOREIGN KEY (user_id) REFERENCES users (id),
  CONSTRAINT post_like_post FOREIGN KEY (post_id) REFERENCES posts (id)
);

CREATE TABLE IF NOT EXISTS post_tags (
  id int NOT NULL,
  post_id int NOT NULL,
  tag_id int NOT NULL,

  PRIMARY KEY (id),
  CONSTRAINT post_tag_post FOREIGN KEY (post_id) REFERENCES posts (id),
  CONSTRAINT post_tag FOREIGN KEY (tag_id) REFERENCES tags (id)
);

CREATE TABLE IF NOT EXISTS comments (
  id int NOT NULL,
  
  owner_id int NOT NULL,
  post_id int NOT NULL,
  body varchar(500) NOT NULL,
  uuid varchar(255) UNIQUE,
  date_created datetime,

  PRIMARY KEY (id),
  CONSTRAINT comment_owner FOREIGN KEY (owner_id) REFERENCES users (id),
  CONSTRAINT comment_post FOREIGN KEY (post_id) REFERENCES posts (id)
);

CREATE TABLE IF NOT EXISTS comment_likes (
  id int NOT NULL,
  
  user_id int NOT NULL,
  comment_id int NOT NULL,
  uuid varchar(255) UNIQUE,
  date_created datetime,

  PRIMARY KEY (id),
  CONSTRAINT comment_like_user FOREIGN KEY (user_id) REFERENCES users (id),
  CONSTRAINT comment_like_comment FOREIGN KEY (comment_id) REFERENCES comments (id)
);

CREATE TABLE IF NOT EXISTS comment_tags (
  id int NOT NULL,
  comment_id int NOT NULL,
  tag_id int NOT NULL,

  PRIMARY KEY (id),
  CONSTRAINT comment_tag_comment FOREIGN KEY (comment_id) REFERENCES comments (id),
  CONSTRAINT comment_tag FOREIGN KEY (tag_id) REFERENCES tags (id)
);

CREATE TABLE IF NOT EXISTS messages (
  id int NOT NULL,
  
  sender_id int NOT NULL,
  recipient_id int NOT NULL,
  content varchar(255) NOT NULL,
  date_sent datetime,
  date_read datetime,
  uuid varchar(255) UNIQUE,
  date_created datetime,

  PRIMARY KEY (id),
  CONSTRAINT message_sender FOREIGN KEY (sender_id) REFERENCES users (id),
  CONSTRAINT message_recipient FOREIGN KEY (recipient_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS notifications (
  id int NOT NULL,

  from_id int,
  user_id int NOT NULL,
  action_type varchar(255) NOT NULL,
  target_type varchar(255),
  target_id int,
  link varchar(255),
  uuid varchar(255) UNIQUE,
  date_created datetime,

  PRIMARY KEY (id),
  CONSTRAINT notification_from FOREIGN KEY (from_id) REFERENCES users (id),
  CONSTRAINT notification_user FOREIGN KEY (user_id) REFERENCES users (id)
);
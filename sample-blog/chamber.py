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

def apply_notification_message(data):
    if data['action_type'] == action_types['follow']:
        data['notification_message'] = data['from']['username'] + ' started following you.'
        data['link'] = '/users/' + str(data['from']['id'])
    if data['action_type'] == action_types['post_like']:
        data['notification_message'] = data['from']['username'] + ' liked your post.'
        data['link'] = '/posts/' + str(data['target_id'])
    if data['action_type'] == action_types['new_comment']:
        data['notification_message'] = data['from']['username'] + ' commented on your post.'
        data['link'] = '/comments/' + str(data['target_id'])
    if data['action_type'] == action_types['comment_like']:
        data['notification_message'] = data['from']['username'] + ' liked your comment.'
        data['link'] = '/comments/' + str(data['target_id'])
    if data['action_type'] == action_types['new_message']:
        data['notification_message'] = data['from']['username'] + ' sent you a message.'
        data['link'] = '/messages/' + str(data['from']['id']) + '-' + str(data['target_id'])
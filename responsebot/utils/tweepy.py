from datetime import datetime


def tweepy_list_to_json(tweepy_list):
    json = dict(tweepy_list.__dict__)

    json.pop('_api')
    # Set default timezone to +0000 here since datetime does not contain tz info
    json['created_at'] = datetime.strftime(json['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    json['user'] = json['user']._json

    return json

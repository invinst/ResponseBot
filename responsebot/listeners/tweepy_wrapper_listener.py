from tweepy.streaming import StreamListener

from responsebot.models import Tweet


class TweepyWrapperListener(StreamListener):
    def __init__(self, listener, *args, **kwargs):
        super(TweepyWrapperListener, self).__init__(*args, **kwargs)

        self.listener = listener

    def on_status(self, status):
        self.listener.on_tweet(Tweet(status._json))

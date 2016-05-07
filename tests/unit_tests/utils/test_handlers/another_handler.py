from responsebot.handlers.base import BaseTweetHandler


class AnotherHandlerClass(BaseTweetHandler):
    def on_tweet(self, tweet):
        print('AnotherHandlerClass')

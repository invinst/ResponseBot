from responsebot.handlers.base import BaseTweetHandler


class HandlerClass(BaseTweetHandler):
    def on_tweet(self, tweet):
        print('HandlerClass')


class HandlerClass2(BaseTweetHandler):
    def on_tweet(self, tweet):
        print('HandlerClass2')


class NonHandlerClass(object):
    def on_tweet(self, tweet):
        print('NonHandlerClass')

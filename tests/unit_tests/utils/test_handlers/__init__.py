from responsebot.handlers.base import BaseTweetHandler


class HandlerClassInInit(BaseTweetHandler):
    def on_tweet(self, tweet):
        print('HandlerClassInInit')

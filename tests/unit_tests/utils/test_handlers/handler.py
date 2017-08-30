from responsebot.handlers import BaseTweetHandler, register_handler


@register_handler
class HandlerClass(BaseTweetHandler):
    def on_tweet(self, tweet):
        print('HandlerClass')


@register_handler
class HandlerClass2(BaseTweetHandler):
    def on_tweet(self, tweet):
        print('HandlerClass2')


class NonRegisteredHandlerClass(BaseTweetHandler):
    def on_tweet(self, tweet):
        print('NonHandlerClass')

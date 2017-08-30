from responsebot.handlers import BaseTweetHandler, register_handler


@register_handler
class AnotherHandlerClass(BaseTweetHandler):
    def on_tweet(self, tweet):
        print('AnotherHandlerClass')

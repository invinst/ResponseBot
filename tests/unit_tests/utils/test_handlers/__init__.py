from responsebot.handlers import BaseTweetHandler, register_handler


@register_handler
class HandlerClassInInit(BaseTweetHandler):
    def on_tweet(self, tweet):
        print('HandlerClassInInit')

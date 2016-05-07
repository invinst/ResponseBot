import sqlite3

from responsebot.handlers.base import BaseTweetHandler


class SaveTweetHandler(BaseTweetHandler):
    def __init__(self, *args, **kwargs):
        super(SaveTweetHandler, self).__init__(*args, **kwargs)

        self.conn = sqlite3.connect('examples/example.db')
        self.c = self.conn.cursor()

    def on_tweet(self, tweet):
        self.c.execute("CREATE TABLE IF NOT EXISTS tweets (tweet text, username text)")
        self.c.execute("INSERT INTO tweets VALUES ('{tweet}', '{username}')".format(
                tweet=tweet.text, username=tweet.user.screen_name))

        self.conn.commit()

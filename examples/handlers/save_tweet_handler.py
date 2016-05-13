# Copyright 2016 Invisible Institute
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sqlite3

from responsebot.handlers.base import BaseTweetHandler


class SaveTweetHandler(BaseTweetHandler):
    def __init__(self, *args, **kwargs):
        super(SaveTweetHandler, self).__init__(*args, **kwargs)

        self.conn = sqlite3.connect('examples/example.db')
        self.c = self.conn.cursor()

    def on_tweet(self, tweet):
        self.c.execute("CREATE TABLE IF NOT EXISTS tweets (tweet text, username text)")
        self.c.execute(u"INSERT INTO tweets VALUES ('{tweet}', '{username}')".format(
                tweet=tweet.text, username=tweet.user.screen_name))

        self.conn.commit()

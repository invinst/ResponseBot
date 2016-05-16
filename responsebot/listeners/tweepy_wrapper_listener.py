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

from tweepy.streaming import StreamListener

from responsebot.models import Tweet


class TweepyWrapperListener(StreamListener):
    def __init__(self, listener, *args, **kwargs):
        super(TweepyWrapperListener, self).__init__(*args, **kwargs)

        self.listener = listener

    def on_status(self, status):
        self.listener.on_tweet(Tweet(status._json))

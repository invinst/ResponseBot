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

from unittest.case import TestCase

from responsebot.models import TweetFilter, Tweet


class TweetFilterTestCase(TestCase):
    def setUp(self):
        self.filter = TweetFilter(track=['keyword'], follow=[123])

    def test_match_tracked_keyword(self):
        match = Tweet({'text': 'keyword text', 'entities': {}, 'user': {'id': 1}})
        unmatched = Tweet({'text': 'text otherkey', 'entities': {}, 'user': {'id': 1}})

        self.assertTrue(self.filter.match_tweet(match))
        self.assertFalse(self.filter.match_tweet(unmatched))

    def test_match_tweet_posters(self):
        match = Tweet({'text': 'text', 'entities': {}, 'user': {'id': 123}})
        unmatched = Tweet({'text': 'text', 'entities': {}, 'user': {'id': 1}})

        self.assertTrue(self.filter.match_tweet(match))
        self.assertFalse(self.filter.match_tweet(unmatched))

    def test_match_user_mentions(self):
        match = Tweet({'text': 'text', 'entities': {'user_mentions': [{'id': 123}]}, 'user': {'id': 1}})
        unmatched = Tweet({'text': 'text', 'entities': {'user_mentions': [{'id': 1}]}, 'user': {'id': 1}})

        self.assertTrue(self.filter.match_tweet(match))
        self.assertFalse(self.filter.match_tweet(unmatched))

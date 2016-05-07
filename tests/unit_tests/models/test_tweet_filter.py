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

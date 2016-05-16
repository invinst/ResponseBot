from unittest.case import TestCase

from responsebot.models import TweetFilter, Tweet


class TweetFilterTestCase(TestCase):
    def setUp(self):
        self.filter = TweetFilter(track=['keyword'], follow=[123])

    def test_match_tracked_keyword(self):
        match = Tweet({'text': 'keyword text', 'entities': {}, 'user': {'id': 1}})
        unmatched = Tweet({'text': 'text otherkey', 'entities': {}, 'user': {'id': 1}})

        self.assertTrue(self.filter.match_tweet(match, user_stream=False))
        self.assertFalse(self.filter.match_tweet(unmatched, user_stream=False))

    def test_match_tweet_posters(self):
        match = Tweet({'text': 'text', 'entities': {}, 'user': {'id': 123}})
        unmatched = Tweet({'text': 'text', 'entities': {}, 'user': {'id': 1}})

        self.assertTrue(self.filter.match_tweet(match, user_stream=False))
        self.assertFalse(self.filter.match_tweet(unmatched, user_stream=False))

    def test_match_user_mentions(self):
        match = Tweet({'text': 'text', 'entities': {'user_mentions': [{'id': 123}]}, 'user': {'id': 1}})
        unmatched = Tweet({'text': 'text', 'entities': {'user_mentions': [{'id': 1}]}, 'user': {'id': 1}})

        self.assertTrue(self.filter.match_tweet(match, user_stream=False))
        self.assertFalse(self.filter.match_tweet(unmatched, user_stream=False))

    def test_match_user_stream_no_track(self):
        self.filter = TweetFilter(track=[])
        match = Tweet({'text': 'keyword text', 'entities': {}, 'user': {'id': 1}})
        unmatched = Tweet({'text': 'text otherkey', 'entities': {}, 'user': {'id': 1}})

        self.assertTrue(self.filter.match_tweet(match, user_stream=True))
        self.assertTrue(self.filter.match_tweet(unmatched, user_stream=True))

    def test_match_user_stream_with_track(self):
        match = Tweet({'text': 'keyword text', 'entities': {}, 'user': {'id': 1}})
        unmatched = Tweet({'text': 'text otherkey', 'entities': {}, 'user': {'id': 1}})

        self.assertTrue(self.filter.match_tweet(match, user_stream=True))
        self.assertFalse(self.filter.match_tweet(unmatched, user_stream=True))

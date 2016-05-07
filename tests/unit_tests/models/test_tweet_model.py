from unittest.case import TestCase

from dateutil.parser import parse

from responsebot.models import Tweet, User


class TweetModelTestCase(TestCase):
    def test_create_from_raw_data(self):
        created_at = 'Mon Apr 25 08:25:58 +0000 2016'
        raw = {
            'some_key': 'some value',
            'created_at': created_at,
            'user': {
                'name': 'Bird'
            },
            'retweeted_status': {
                'created_at': created_at,
            },
            'quoted_status': {
                'created_at': created_at,
            }
        }

        tweet = Tweet(raw)

        expected_created_at = parse(created_at)

        self.assertEqual(tweet.some_key, 'some value')
        self.assertEqual(tweet.created_at, expected_created_at)

        self.assertTrue(isinstance(tweet.user, User))
        self.assertEqual(tweet.user.name, 'Bird')

        self.assertTrue(isinstance(tweet.retweeted_tweet, Tweet))
        self.assertEqual(tweet.retweeted_tweet.created_at, expected_created_at)

        self.assertTrue(isinstance(tweet.quoted_tweet, Tweet))
        self.assertEqual(tweet.quoted_tweet.created_at, expected_created_at)

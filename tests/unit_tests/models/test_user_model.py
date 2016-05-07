from unittest.case import TestCase

from dateutil.parser import parse

from responsebot.models import User, Tweet


class UserModelTestCase(TestCase):
    def test_create_from_raw_data(self):
        created_at = 'Mon Apr 25 08:25:58 +0000 2016'
        raw = {
            'some_key': 'some value',
            'created_at': created_at,
            'status': {
                'created_at': created_at
            },
            'following': True
        }

        expected_created_at = parse(created_at)

        user = User(raw)

        self.assertEqual(user.some_key, 'some value')
        self.assertEqual(user.created_at, expected_created_at)

        self.assertTrue(isinstance(user.tweet, Tweet))
        self.assertEqual(user.tweet.created_at, expected_created_at)

        self.assertEqual(user.following, True)

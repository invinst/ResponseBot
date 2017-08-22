from unittest.case import TestCase

from dateutil.parser import parse

from responsebot.models import List, User


class ListModelTestCase(TestCase):
    def test_parse_list(self):
        created_at = 'Mon Apr 25 08:25:58 +0000 2016'
        raw = {
            'some_key': 'some value',
            'created_at': created_at,
            'user': {
                'screen_name': 'some_one'
            }
        }

        expected_created_at = parse(created_at)

        list = List(raw)

        self.assertEqual(list.some_key, 'some value')
        self.assertEqual(list.created_at, expected_created_at)

        self.assertTrue(isinstance(list.user, User))
        self.assertEqual(list.user.screen_name, 'some_one')

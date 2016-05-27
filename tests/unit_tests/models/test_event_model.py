from unittest.case import TestCase

from dateutil.parser import parse

from responsebot.models import Event, User, Tweet, List


class EventModelTestCase(TestCase):
    def test_create_from_raw_data(self):
        created_at = 'Mon Apr 25 08:25:58 +0000 2016'
        raw = {
            'event': 'some value',
            'created_at': created_at,
            'target': {
                'name': 'target'
            },
            'source': {
                'name': 'source',
            }
        }

        event = Event(raw)

        expected_created_at = parse(created_at)

        self.assertEqual(event.event, 'some value')
        self.assertEqual(event.created_at, expected_created_at)

        self.assertTrue(isinstance(event.target, User))
        self.assertEqual(event.target.name, 'target')

        self.assertTrue(isinstance(event.source, User))
        self.assertEqual(event.source.name, 'source')

        self.assertIsNone(event.target_object)

    def test_parse_target_object(self):
        for event_type in ['follow', 'unfollow', 'block', 'unblock', 'user_update']:
            raw_event = {
                'event': event_type
            }
            event = Event(raw_event)
            self.assertIsNone(event.target_object)

        for event_type in ['favorite', 'unfavorite', 'quoted_tweet']:
            raw_event = {
                'event': event_type,
                'target_object': {
                    'something': 'some value'
                }
            }
            event = Event(raw_event)
            self.assertTrue(isinstance(event.target_object, Tweet))
            self.assertEqual(event.target_object.something, 'some value')

        for event_type in ['list_created', 'list_destroyed', 'list_updated', 'list_member_added',
                'list_member_removed', 'list_user_subscribed', 'list_user_unsubscribed']:
            raw_event = {
                'event': event_type,
                'target_object': {
                    'something': 'some value'
                }
            }
            event = Event(raw_event)
            # TODO: will update test after creating List model
            self.assertTrue(isinstance(event.target_object, List))
            self.assertEqual(event.target_object.something, 'some value')

        for event_type in ['access_revoked']:
            raw_event = {
                'event': event_type,
                'target_object': {
                    'something': 'some value'
                }
            }
            event = Event(raw_event)
            self.assertTrue(isinstance(event.target_object, dict))
            self.assertEqual(event.target_object['something'], 'some value')

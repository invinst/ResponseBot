from unittest import TestCase

from tests.unit_tests.utils.test_handlers import HandlerClassInInit
from tests.unit_tests.utils.test_handlers.another_handler import AnotherHandlerClass

from responsebot.handlers.base import BaseTweetHandler
from responsebot.utils.handler_utils import is_handler_class, discover_handler_classes
from tests.unit_tests.utils.test_handlers.handler import HandlerClass, NonHandlerClass, HandlerClass2


class DiscoverHandlerClassesTestCase(TestCase):
    def test_discover_handler_classes(self):
        handler_classes = discover_handler_classes('tests.unit_tests.utils.test_handlers')

        # discover handler class in package init
        self.assertIn(HandlerClassInInit, handler_classes)

        # discover handler class in handler
        self.assertIn(HandlerClass, handler_classes)
        self.assertIn(HandlerClass2, handler_classes)
        self.assertNotIn(NonHandlerClass, handler_classes)

        # discover handler class in multiple modules
        self.assertIn(AnotherHandlerClass, handler_classes)

    def test_discover_handler_classes_in_module(self):
        handler_classes = discover_handler_classes('tests.unit_tests.utils.test_handlers.handler')

        # discover handler class in handler
        self.assertIn(HandlerClass, handler_classes)
        self.assertIn(HandlerClass2, handler_classes)
        self.assertNotIn(NonHandlerClass, handler_classes)


class IsHandlerClassTestCase(TestCase):
    def test_with_handler_class(self):
        self.assertTrue(is_handler_class(HandlerClass))

    def test_with_non_handler_class(self):
        self.assertFalse(is_handler_class(NonHandlerClass))

    def test_with_non_class_obj(self):
        self.assertFalse(is_handler_class({}))

    def test_with_base_class(self):
        self.assertFalse(is_handler_class(BaseTweetHandler))

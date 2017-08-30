from unittest import TestCase

from tests.unit_tests.utils.test_handlers import HandlerClassInInit
from tests.unit_tests.utils.test_handlers.another_handler import AnotherHandlerClass

from responsebot.utils.handler_utils import discover_handler_classes
from tests.unit_tests.utils.test_handlers.handler import HandlerClass, NonRegisteredHandlerClass, HandlerClass2


class DiscoverHandlerClassesTestCase(TestCase):
    def test_discover_handler_classes(self):
        handler_classes = discover_handler_classes('tests.unit_tests.utils.test_handlers')

        # discover handler class in package init
        self.assertIn(HandlerClassInInit, handler_classes)

        # discover handler class in handler
        self.assertIn(HandlerClass, handler_classes)
        self.assertIn(HandlerClass2, handler_classes)
        self.assertNotIn(NonRegisteredHandlerClass, handler_classes)

        # discover handler class in multiple modules
        self.assertIn(AnotherHandlerClass, handler_classes)

    def test_discover_handler_classes_in_module(self):
        handler_classes = discover_handler_classes('tests.unit_tests.utils.test_handlers.handler')

        # discover handler class in handler
        self.assertIn(HandlerClass, handler_classes)
        self.assertIn(HandlerClass2, handler_classes)
        self.assertNotIn(NonRegisteredHandlerClass, handler_classes)

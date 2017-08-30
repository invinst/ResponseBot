from .base import BaseTweetHandler
from .event import BaseEventHandler


registered_handlers = set()


def register_handler(handler_class):
    registered_handlers.add(handler_class)
    return handler_class

from __future__ import absolute_import

import logging

import sys

from responsebot.common.exceptions import MissingConfigError, AuthenticationError, APIQuotaError, \
    UserHandlerError, APIError
from responsebot.listeners.responsebot_listener import ResponseBotListener
from responsebot.responsebot_stream import ResponseBotStream
from responsebot.utils import handler_utils, auth_utils
from responsebot.utils.config_utils import ResponseBotConfig
from responsebot.utils.log_utils import configure_logging


class ResponseBot(object):
    """
    The entry point of ResponseBot. :func:`~responsebot.responsebot.ResponseBot.__init__` inits & configures the bot.
    :func:`~responsebot.responsebot.ResponseBot.start` tries to init the main sub-components (handler discoverer,
    authenticator, tweet streamer, etc.) and handle errors if necessary
    """
    def __init__(self, *args, **kwargs):
        """
        Try to init & configure the bot from configurations read from ``.responsebot`` file, from CLI arguments or from
        direct call in code

        :param kwargs: Options for :class:`~responsebot.utils.config_utils.ResponseBotConfig`
        """
        configure_logging()
        try:
            self.config = ResponseBotConfig(*args, **kwargs)
        except MissingConfigError as e:
            logging.error(str(e))
            sys.exit()

    def start(self):
        """
        Try to init the main sub-components (:func:`~responsebot.utils.handler_utils.discover_handler_classes`, \
        :func:`~responsebot.utils.auth_utils.auth`, :class:`~responsebot.responsebot_stream.ResponseBotStream`, etc.)
        """
        logging.info('ResponseBot started')

        try:
            handler_classes = handler_utils.discover_handler_classes(self.config.get('handlers_package'))
            if len(handler_classes) == 0:
                logging.warning('No handler found. Did you forget to extend BaseTweethandler? Check --handlers-module')
        except ImportError as e:
            logging.error(str(e))
            sys.exit()

        try:
            client = auth_utils.auth(
                consumer_key=self.config.get('consumer_key'),
                consumer_secret=self.config.get('consumer_secret'),
                token_key=self.config.get('token_key'),
                token_secret=self.config.get('token_secret'),
            )
        except (APIQuotaError, AuthenticationError) as e:
            logging.error(str(e))
            sys.exit()

        try:
            listener = ResponseBotListener(client=client, handler_classes=handler_classes)

            stream = ResponseBotStream(client=client, listener=listener)
            stream.start()
        except UserHandlerError as e:
            # TODO: print only stack trace from user exception
            logging.exception(e)
            sys.exit()
        except APIError as e:
            logging.error(str(e))
            sys.exit()

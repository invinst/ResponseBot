from __future__ import absolute_import

import logging

import sys
import datetime
import time

from responsebot.common.exceptions import MissingConfigError, AuthenticationError, APIQuotaError, APIError
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

        self.error_time_log = {}
        self.error_sleep_log = {}

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

        while True:
            try:
                client = auth_utils.auth(self.config)

                listener = ResponseBotListener(client=client, handler_classes=handler_classes)

                stream = ResponseBotStream(client=client, listener=listener)
                stream.start()
            except (APIQuotaError, AuthenticationError, APIError) as e:
                self.handle_error(e)
            else:
                break

    def handle_error(self, error):
        """
        Try to detect repetitive errors and sleep for a while to avoid being marked as spam
        """
        error_desc = str(error)
        now = datetime.datetime.now()
        if error_desc not in self.error_time_log:
            self.error_time_log[error_desc] = now
            return

        time_of_last_encounter = self.error_time_log[str(error)]
        time_since_last_encounter = now - time_of_last_encounter
        if time_since_last_encounter.total_seconds() > self.config.get('min_seconds_between_errors'):
            self.error_time_log[error_desc] = now
            return

        if error_desc not in self.error_sleep_log:
            time.sleep(self.config.get('sleep_seconds_on_consecutive_errors'))
            self.error_sleep_log[error_desc] = 1
        else:
            logging.error(error_desc)
            sys.exit()

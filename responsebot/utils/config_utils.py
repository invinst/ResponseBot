# Copyright 2016 Invisible Institute
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Utilities for handling configurations
"""
from responsebot.common.exceptions import MissingConfigError

try:
    from ConfigParser import SafeConfigParser
except ImportError:
    from configparser import SafeConfigParser


class ResponseBotConfig(object):
    """Get config values and validate them."""
    REQUIRED_CONFIGS = ['handlers_package', 'consumer_key', 'consumer_secret', 'token_key', 'token_secret']
    CONFIG_FILE = '.responsebot'

    def __init__(self, *args, **kwargs):
        """
        :param kwargs: Config from CLI arguments
        """
        self._config = {}
        self.load_config_file()
        self.load_config_from_cli_arguments(*args, **kwargs)
        self.validate_configs()

    def load_config_file(self):
        """Parse configuration file and get config values."""
        config_parser = SafeConfigParser()

        config_parser.read(self.CONFIG_FILE)

        if config_parser.has_section('handlers'):
            self._config['handlers_package'] = config_parser.get('handlers', 'package')

        if config_parser.has_section('auth'):
            self._config['consumer_key'] = config_parser.get('auth', 'consumer_key')
            self._config['consumer_secret'] = config_parser.get('auth', 'consumer_secret')
            self._config['token_key'] = config_parser.get('auth', 'token_key')
            self._config['token_secret'] = config_parser.get('auth', 'token_secret')

        if config_parser.has_section('stream'):
            self._config['user_stream'] = config_parser.get('stream', 'user_stream').lower() == 'true'
        else:
            self._config['user_stream'] = False

    def load_config_from_cli_arguments(self, *args, **kwargs):
        """
        Get config values of passed in CLI options.

        :param dict kwargs: CLI options
        """
        self._load_config_from_cli_argument(key='handlers_package', **kwargs)
        self._load_config_from_cli_argument(key='auth', **kwargs)
        self._load_config_from_cli_argument(key='user_stream', **kwargs)

    def _load_config_from_cli_argument(self, key, **kwargs):
        if kwargs.get(key):
            if key == 'auth':
                self._config['consumer_key'], self._config['consumer_secret'],\
                self._config['token_key'], self._config['token_secret'] = kwargs.get(key)
            else:
                self._config[key] = kwargs.get(key)

    def validate_configs(self):
        """
        Check that required config are set.
        :raises :class:`~responsebot.common.exceptions.MissingConfigError`: if a required config is missing
        """
        # Check required arguments, validate values
        for conf in self.REQUIRED_CONFIGS:
            if conf not in self._config:
                raise MissingConfigError('Missing required configuration %s' % conf)

    def get(self, key):
        """
        Get config value specify by key.

        :param str key: config key
        :return: config value
        """
        return self._config[key]

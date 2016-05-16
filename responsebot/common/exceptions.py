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
Exceptions and errors used by Tweet Bot
"""


class ResponseBotError(Exception):
    """Generic response bot error."""
    pass


class NotFreeToTweetError(ResponseBotError):
    """
    Error to indicate Tweeter fails to post some status due to Twitter API's status update rate limit.
    """
    pass


class MissingConfigError(ResponseBotError):
    """
    Exception to indicate a required configuration for Tweet Bot is not found from config file or CLI.
    """
    pass


class AuthenticationError(ResponseBotError):
    """
    Error to indicate Tweet Bot failed to authenticate with the provided credentials.
    """
    pass


class APIError(ResponseBotError):
    """Generic API error."""
    pass


class APIQuotaError(APIError):
    """
    Exception indicate some API quota breached.
    """
    pass


class UnknownAPIError(APIError):
    """
    Unknown error when executing API.
    """
    pass


class UserHandlerError(ResponseBotError):
    """
    Error to indicate some error caused by a user's handler.
    """
    def __init__(self, user_exception, msg='Error from user handler', *args, **kwargs):
        super(UserHandlerError, self).__init__(msg, *args, **kwargs)
        self.__cause__ = user_exception

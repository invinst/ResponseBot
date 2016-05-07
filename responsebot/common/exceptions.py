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
    def __init__(self, msg='Error from user handler', *args, **kwargs):
        super(UserHandlerError, self).__init__(msg, *args, **kwargs)

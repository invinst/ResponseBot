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


class AutomatedRequestError(ResponseBotError):
    """
    Error to indicate a request is deemed automated by Twitter.
    """
    pass


class OverCapacityError(ResponseBotError):
    """
    Error to indicate Twitter is currently over capacity.
    """
    pass


class DailyStatusUpdateError(ResponseBotError):
    """
    Error to indicate your account reached the daily status update limit.
    """
    pass


class CharacterLimitError(ResponseBotError):
    """
    Error to indicate your tweet reached the character limit.
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

from responsebot.models import TweetFilter


class BaseTweetHandler(object):
    """
    An abstract base tweet handler class for the user to subclass.
    """

    def __init__(self, client=None, *args, **kwargs):
        """

        :param client: Some Twitter API client for authentication. E.g. :class:`~responsebot.tweet_client.TweetClient`
        """
        self.catch_self_tweets = False
        self.client = client
        self.filter = self.get_filter()

    def get_filter(self):
        """
        Override this method for custom filter
        """
        return TweetFilter(follow=[str(self.client.get_current_user().id)])

    def on_tweet(self, tweet):
        """
        Callback for when a tweet appears in user timeline

        :param tweet: The incoming tweet
        :type tweet: :class:`~responsebot.models.Tweet`
        """
        raise NotImplementedError

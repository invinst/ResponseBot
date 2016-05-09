# ResponseBot

## Description
An open source framework for developing listen-and-answer twitter bots.

## Installation
```
$ pip install responsebot
```

## Examples
### Basic usage
* Create a class to handle incoming tweet

```python
from responsebot.handlers.base import BaseTweetHandler


class MyTweetHandler(BaseTweetHandler):
    def on_tweet(self, tweet):
        print('Received tweet: %s from %s' % (tweet.text, tweet.user.screen_name))
```

* Create a `.responsebot` file in your project root with your Twitter API credentials (which can be obtained after you created a Twitter application [here](https://apps.twitter.com/))

```
[auth]
consumer_key = <consumer_key>
consumer_secret = <consumer_secret>
token_key = <token_key>
token_secret = <token_secret>
```

* Run in your project root

```
$ start_responsebot --handlers-package <path to your python module>
```

* Or use responsebot as a library

```python
from responsebot.responsebot import ResponseBot


ResponseBot(handlers_package='<path to your python module>').start()
```

## [Documentation](http://responsebot.readthedocs.org)

import logging
import logging.config


# TODO: add rotate file log
DEFAULT_CONFIG = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '[%(levelname)s] %(asctime)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    }
}


def configure_logging():
    logging.config.dictConfig(DEFAULT_CONFIG)

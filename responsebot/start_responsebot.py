from __future__ import absolute_import

import click
import dotenv

from responsebot.responsebot import ResponseBot


# Click is not working properly on Python 3, we have to load locale env to work
dotenv.load_dotenv('.env')


@click.command()
@click.option('--handlers-package', help='Path to package containing all your handlers')
def main(*args, **kwargs):
    """Run responsebot"""
    # TODO: validate options
    # TODO: options for credentials
    ResponseBot(*args, **kwargs).start()

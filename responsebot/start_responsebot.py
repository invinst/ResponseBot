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

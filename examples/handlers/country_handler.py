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

import json

from responsebot.handlers.base import BaseTweetHandler


class CountryHandler(BaseTweetHandler):
    def __init__(self, *args, **kwargs):
        super(CountryHandler, self).__init__(*args, **kwargs)

        self.countries = json.load(open('examples/countries.json'))['country']
        self.countries = {
            x['countryName']: {
                'population': x['population'],
                'languages': x['languages'],
                'continentName': x['continentName']
            } for x in self.countries
        }

    def on_tweet(self, tweet):
        country = ' '.join(tweet.text.split(' ')[1:])

        if country in self.countries:
            info = self.countries[country]
            self.client.tweet(
                'Country: {country}\n'
                'Population: {population}\n'
                'Languages: {languages}\n'
                'Continent: {continent}'.format(
                    country=country,
                    population=info['population'],
                    languages=info['languages'],
                    continent=info['continentName']
                )
            )

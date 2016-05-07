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

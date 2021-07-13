from setuptools import setup

setup(name='Hate Tweet Map',
      version='1.0',
      description='Python Distribution Utilities',
      author='Dario Amoroso d\'Aragona',
      packages=['hate_tweet_map.database', 'hate_tweet_map.util','hate_tweet_map', 'hate_tweet_map.tweets_searcher', 'hate_tweet_map.tweets_processor',
                'hate_tweet_map.users_searcher'],
      install_requires=[
          'geocoder == 1.38.1',
          'pandas == 1.2.4',
          'pymongo == 3.11.4',
          'python-dateutil == 2.8.1',
          'PyYAML == 5.4.1',
          'requests == 2.25.1',
          'six == 1.15.0',
          'tqdm == 4.60.0',
          'setuptools >= 56.0.0',
          'feel-it'
      ],
      test_suite='tests'
      )

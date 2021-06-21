import logging
from datetime import datetime

from hate_tweet_map.database import DataBase
from SearchTweets import SearchTweets
import time


def main():
    logging.basicConfig()
    log = logging.getLogger("SEARCH")
    log.setLevel(logging.INFO)
    start = time.time()
    log.info(datetime.fromtimestamp(start))

    mongo_db = DataBase("search_tweets.config")
    log.info("LOADING CONFIGURATION")
    twitter_search = SearchTweets(mongo_db)

    log.info("SEARCH FOR TWEETS")
    n_tweets = twitter_search.search()

    log.info("TWEETS FOUND AND SAVED SUCCESSFULLY: {}".format(n_tweets))

    end = time.time()
    log.info("DONE IN: {}".format(end - start))


if __name__ == "__main__":
    main()

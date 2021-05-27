import logging
from TwitterSearch import TwitterSearch
import time


def main():
    logging.basicConfig()
    log = logging.getLogger("SEARCH")
    log.setLevel(logging.INFO)
    start = time.time()

    log.info("LOADING CONFIGURATION")
    twitter_search = TwitterSearch()

    log.info("SEARCH FOR TWEETS")
    n_tweets = twitter_search.search()

    log.info("TWEETS FOUND AND SAVED SUCCESSFULLY: {}".format(n_tweets))

    end = time.time()
    log.info("DONE IN: {}".format(end - start))


if __name__ == "__main__":
    main()

import concurrent
import logging
from concurrent.futures import ThreadPoolExecutor, Future, as_completed

from tqdm import tqdm

from DataBase import DataBase
from TwitterSearch import TwitterSearch
import time
import util


def main():
    logging.basicConfig()
    log = logging.getLogger("SEARCH")
    log.setLevel(logging.INFO)
    start = time.time()

    log.info("LOADING CONFIGURATION")
    twitter_search = TwitterSearch()

    log.info("SEARCH FOR TWEETS")
    twitter_results = twitter_search.search()
    mongo_db = DataBase()
    log.info("SAVING TWEETS")
    for response in twitter_results:
        if 'data' in response:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for tweet in (response['data']):
                    futures = []
                    if not mongo_db.is_in(tweet['id']):
                        future = executor.submit(pre_process, tweet, response)
                        future.add_done_callback(save)
                        futures.append(future)
    end = time.time()
    log.info("DONE IN: {}".format(end - start))


def save(future: Future):
    mongo_db = DataBase()
    mongo_db.save_one(future.result())


def pre_process(tweet, response):
    return util.pre_process_response(tweet, response['includes'])


if __name__ == "__main__":
    main()

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
    twitter_search.search()

    end = time.time()
    log.info("DONE IN: {}".format(end - start))



if __name__ == "__main__":
    main()

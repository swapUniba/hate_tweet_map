import concurrent
from concurrent.futures import ThreadPoolExecutor

from tqdm import tqdm

from DataBase import DataBase
from TwitterSearch import TwitterSearch
import time
import util


def main():
    start = time.time()

    print("[1/2] Configuring twitter API...")
    twitter_search = TwitterSearch()

    print("[2/2] Searching for tweets...")
    twitter_results = twitter_search.search()
    mongo_db = DataBase()
    for response in twitter_results:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for tweet in tqdm(response['data']):
                futures.append(executor.submit(pre_process(mongo_db, tweet, response)))

    end = time.time()
    print("done in: {}".format(end - start))


def pre_process(mongo_db, tweet, response):
    if mongo_db.is_in(tweet['id']):
        return
    mongo_db.save_one(util.pre_process_response(tweet, response['includes']))


if __name__ == "__main__":
    main()

import concurrent
from concurrent.futures import ThreadPoolExecutor, Future, as_completed

from tqdm import tqdm

from DataBase import DataBase
from TwitterSearch import TwitterSearch
import time
import util


def main():
    start = time.time()

    print("[1/3] Configuring twitter API...")
    twitter_search = TwitterSearch()

    print("[2/3] Searching for tweets...")
    twitter_results = twitter_search.search()
    mongo_db = DataBase()
    print("[3/3] pre-processing tweets...")

    for response in twitter_results:
        print("[3/3] pre-processing tweets: {}".format(len(response['data'])))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for tweet in (response['data']):
                futures = []
                if not mongo_db.is_in(tweet['id']):
                    future = executor.submit(pre_process, tweet, response)
                    future.add_done_callback(save)
                    futures.append(future)
            for job in tqdm(as_completed(futures), total=len(futures)):
                pass

    end = time.time()
    print("done in: {}".format(end - start))


def save(future: Future):
    mongo_db = DataBase()
    mongo_db.save_one(future.result())


def pre_process(tweet, response):
    return util.pre_process_response(tweet, response['includes'])


if __name__ == "__main__":
    main()

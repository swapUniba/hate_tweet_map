from DataBase import DataBase
from TwitterSearch import TwitterSearch
import time
import util


def main():

    print("[1/2] Configuring twitter API...")
    twitter_search = TwitterSearch()

    print("[2/2] Searching for tweets...")
    twitter_results = twitter_search.search()
    mongo_db = DataBase()
    pre_processed_tweets = util.pre_process_response(twitter_results)
    new_tweet = mongo_db.delete_tweets_already_saved(pre_processed_tweets)
    mongo_db.save_many(new_tweet)


if __name__ == "__main__":
    main()

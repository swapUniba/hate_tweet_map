import yaml
from pymongo import MongoClient
from yaml import BaseLoader


class DataBase:

    def __init__(self):
        with open("config.yml", "r") as yamlfile:
            cfg = yaml.load(yamlfile, Loader=BaseLoader)

            self.__mongo_db_url = cfg['mongodb']['url']
            self.__mongo_db_database_name = cfg['mongodb']['database']
            self.__mongo_db_collection_name = cfg['mongodb']['collection']
            self.__client = MongoClient(self.__mongo_db_url)
            self.__db = self.__client.get_database(self.__mongo_db_database_name)
            self.__collection = self.__db.get_collection(self.__mongo_db_collection_name)

    def delete_tweets_already_saved(self, tweets):
        new_tweet = []
        for tweet in tweets:
            if self.__collection.count_documents({"_id": str(tweet['_id'])}) != 0:
                continue
            new_tweet.append(tweet)
        return new_tweet

    def extract_tweets_to_process(self):

        query = {'processed': str(False)}
        result = []
        for tweet in self.__collection.find(query):
            result.append(tweet)
        return result

    def save_many(self, tweets: []):
        if len(tweets) != 0:
            self.__collection.insert_many(tweets)

    def save_one(self, tweet: {}):
        self.__collection.insert_one(tweet)

    def update_one(self, tweet):
        query = {"_id": tweet['_id']}
        self.__collection.replace_one(query, tweet)

    def is_in(self, id: ""):
        return self.__collection.count_documents({"_id": id}) > 0
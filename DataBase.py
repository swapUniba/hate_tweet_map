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

    def delete_tweets_already_saved(self, tweets):
        client = MongoClient(self.__mongo_db_url)
        db = client.get_database(self.__mongo_db_database_name)
        collection = db.get_collection(self.__mongo_db_collection_name)
        new_tweet = []
        for tweet in tweets:
            if collection.count_documents({"_id": str(tweet['_id'])}) != 0:
                continue
            new_tweet.append(tweet)
        return new_tweet

    def save(self, tweets=[]):
        client = MongoClient(self.__mongo_db_url)
        db = client.get_database(self.__mongo_db_database_name)
        collection = db.get_collection(self.__mongo_db_collection_name)
        collection.insert_many(tweets)

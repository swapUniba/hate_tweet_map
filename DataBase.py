from json import dumps

import yaml
from pymongo import MongoClient


class DataBase:

    def __init__(self, file_path=""):
        with open(file_path, "r") as yamlfile:
            cfg = yaml.safe_load(yamlfile)

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

    def find_by_id(self, id):
        query = {'_id': id}
        for tweet in self.__collection.find(query):
            return tweet

    def extract(self, query):
        result = []
        for tweet in self.__collection.find(query):
            result.append(tweet)
        return result

    def extract_tweets_not_processed(self):

        query = {'processed': str(False)}
        result = []
        for tweet in self.__collection.find(query):
            result.append(tweet)
        return result

    def extract_all_tweets(self):
        result = []
        for tweet in self.__collection.find():
            result.append(tweet)
        return result

    def extract_all_tweets_to_geo(self):
        result = []
        query = {"$and": [{"city": {"$exists": True}}, {"country": {"$exists": True}}]}
        for tweet in self.__collection.find(query):
            result.append(tweet)
        return result

    def extract_new_tweets_to_geo(self):
        result = []
        query = {"$and": [{"city": {"$exists": True}}, {"country": {"$exists": True}}, {"processed": False},
                          {"coordinates": {"$exists": False}}]}
        for tweet in self.__collection.find(query):
            result.append(tweet)
        return result

    def extract_new_tweets_to_nlp(self):
        result = []
        query = {"processed": False}
        for tweet in self.__collection.find(query):
            result.append(tweet)
        return result

    def extract_new_tweets_to_sentit(self):
        result = []
        query = {"$and": [{"sentiment.sent-it": {"$exists": False}}, {"processed": False}]}
        for tweet in self.__collection.find(query):
            result.append(tweet)
        return result

    def extract_new_tweets_to_tag(self):
        result = []
        query = {"$and": [{"sentiment.tags.tag_me": {"$exists": False}}, {"processed": False}]}
        for tweet in self.__collection.find(query):
            result.append(tweet)
        return result

    def extract_new_tweets_to_feel_it(self):
        result = []
        query = {"$and": [{"sentiment.feel-it": {"$exists": False}}, {"processed": False}]}
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

    def delete_one(self, id: ""):
        self.__collection.delete_one({"_id": id})

    def delete_more(self, query):
        return self.__collection.delete_many(query).deleted_count

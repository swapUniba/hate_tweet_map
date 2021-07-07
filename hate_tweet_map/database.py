import yaml
from pymongo import MongoClient


class DataBase:
    """

    Class to perform operation on the mongodb collection. This class handle the operation on the collection
    containing tweets and the operation on the collection containing the users.

    """

    def __init__(self, file_path="", key="mongodb"):

        with open(file_path, "r") as yamlfile:
            cfg = yaml.safe_load(yamlfile)

            self.__mongo_db_url = cfg[key]['url']
            self.__mongo_db_database_name = cfg[key]['database']
            self.__mongo_db_collection_name = cfg[key]['collection']
            self.__client = MongoClient(self.__mongo_db_url)
            self.__db = self.__client.get_database(self.__mongo_db_database_name)
            self.__collection = self.__db.get_collection(self.__mongo_db_collection_name)

    def find_by_id(self, id):
        query = {'_id': id}
        for tweet in self.__collection.find(query):
            return tweet

    def extract(self, query: dict) -> list[dict]:
        """
        Extract the tweets that match the query from the collection.

        :param query: a query to use to extract tweets from the collection
        :type query: dict
        :return: the tweets extract
        :rtype: list[dict]
        """
        result = []
        for tweet in self.__collection.find(query):
            result.append(tweet)
        return result

    def extract_tweets_not_processed(self) -> list[dict]:
        """
        Extract all the tweets where tha value of the field "processed" is False.
        This means that this tweets have not yet been processed by SpaCy.

        :return: the tweets extract
        :rtype: list[dict]
        """

        query = {'processed': False}
        result = []
        for tweet in self.__collection.find(query):
            result.append(tweet)
        return result

    def extract_all_tweets(self) -> list[dict]:
        """
        Extract all the tweets in the collection sorting it by language.

        :return: the tweets extract
        :rtype: list[dict]
        """

        result = []
        for tweet in self.__collection.find().sort("lang",-1):
            result.append(tweet)
        return result

    def extract_all_tweets_to_geo(self) -> list[dict]:
        """
        Extract all tweets, already processed or not (nby SpaCy), that contain Twitter geographic information,
        then tweets that have a user_location field or a city and country field.

        :return: the tweets extract
        :rtype: list[dict]
        """

        result = []
        query = {"$or": [{"$and": [{"geo.city": {"$exists": True}}, {"geo.country": {"$exists": True}}]}, {"geo.user_location": {"$exists": True}}]}
        for tweet in self.__collection.find(query):
            result.append(tweet)
        return result

    def extract_new_tweets_to_geo(self) -> list[dict]:
        """
        Extract all tweets, not already processed, that contain Twitter geographic information,
        then tweets not processed (by SpaCy), that have a user_location field or a city and country field, and
        that not have the coordinates.

        :return: the tweets extract
        :rtype: list[dict]
        """

        result = []
        query = {"$and": [{"$or": [{"$and": [{"geo.city": {"$exists": True}}, {"geo.country": {"$exists": True}}]}, {"geo.user_location": {"$exists": True}}]}, {"processed": False},
                          {"geo.coordinates": {"$exists": False}}]}
        for tweet in self.__collection.find(query):
            result.append(tweet)
        return result

    def extract_new_tweets_to_nlp(self) -> list[dict]:
        """
        Extract all tweets, not already processed (by SpaCY).

        :return: the tweets extract
        :rtype: list[dict]
        """
        result = []
        query = {"processed": False}
        for tweet in self.__collection.find(query).sort("lang", -1):
            result.append(tweet)
        return result

    def extract_new_tweets_to_sentit(self) -> list[dict]:
        """
        Extract all tweets, not already processed (by SpaCy), that have not yet been analyzed by sent-it,
        so the tweets that not contains the field "sentiment.sent-it" and where the field "processed" is False.

        :return: the tweets extract
        :rtype: list[dict]
        """

        result = []
        query = {"$and": [{"sentiment.sent-it": {"$exists": False}}, {"processed": False}]}
        for tweet in self.__collection.find(query):
            result.append(tweet)
        return result

    def extract_new_tweets_to_tag(self) -> list[dict]:
        """
        Extract all tweets, not already processed (by SpaCy), that have not yet been analyzed by TagMe,
        so the tweets that not contains the field "tags.tag_me" and where the field "processed" is False.

        :return: the tweets extract
        :rtype: list[dict]
        """

        result = []
        query = {"$and": [{"tags.tag_me": {"$exists": False}}, {"processed": False}]}
        for tweet in self.__collection.find(query):
            result.append(tweet)
        return result

    def extract_new_tweets_to_feel_it(self) -> list[dict]:
        """
        Extract all italian tweets, not already processed (by SpaCy), that have not yet been analyzed by feel-it,
        so the tweets that not contains the field "sentiment.feel-it" and where the field "processed" is False and
        where the "lang" field is "it".

        :return: the tweets extract
        :rtype: list[dict]
        """

        result = []
        query = {"$and": [{"sentiment.feel-it": {"$exists": False}}, {"processed": False}, {"lang": "it"}]}
        for tweet in self.__collection.find(query):
            result.append(tweet)
        return result

    def extract_all_tweets_to_feel_it(self) -> list[dict]:
        """
        Extract all italian tweets, already processed (by SpaCy) or not, that have not yet been analyzed by feel-it,
        so the tweets where the "lang" field is "it".

        :return: the tweets extract
        :rtype: list[dict]
        """

        result = []
        query = {"lang": "it"}
        for tweet in self.__collection.find(query):
            result.append(tweet)
        return result

    def save_many(self, tweets: list) -> None:
        """
        Save more than one tweets in the collection.


        :param tweets: the tweets to save
        :type tweets: list
        :return: None
        """

        if len(tweets) != 0:
            self.__collection.insert_many(tweets)

    def save_one(self, tweet: dict) -> None:
        """
        Save one tweet in the collection.

        :param tweet: the tweet to save
        :type tweet: dict
        :return: None
        """

        self.__collection.insert_one(tweet)

    def update_one(self, tweet: dict) -> None:
        """
        Update one tweet in the collection.

        :param tweet: the tweets to update
        :type tweet: dict
        :return: None
        """

        query = {"_id": tweet['_id']}
        self.__collection.replace_one(query, tweet)

    def is_in(self, id: str) -> bool:
        """
        Check if the tweet is in the collection or not

        :param id: the id of tweet to check
        :type id: str
        :return: True if is in, False otherwise
        :rtype: bool
        """

        return self.__collection.count_documents({"_id": id}) > 0

    def delete_one(self, id: str) -> None:
        """
        Delete one tweet from the collection

        :param id: the id of tweet to delete
        :type id: str
        :return: None
        """

        self.__collection.delete_one({"_id": id})

    def delete_more(self, query:dict) -> int:
        """
        Delete all the tweets that match the query given from the collection.

        :param query: the query to find the tweets to delete
        :type query: dict
        :return: number of tweets deleted
        :rtype: int
        """

        return self.__collection.delete_many(query).deleted_count

    def get_users_id(self) -> list[int]:
        """
        For each tweet in tbe collection retrieves the id of the user that posted the tweet.

        :return: a list containing the user's id
        :rtype: list[int]
        """

        result = []
        query = {"author_id": 1, "_id": 0}
        for tweet in self.__collection.find({},query):
            result.append(list(tweet.values())[0])
        return list(set(result))

    def get_users(self) -> list[int]:
        """
         For each user in tbe collection retrieves the id of the user.

         :return: a list containing the user's id
         :rtype: list[int]
         """

        result = []
        query = {"_id": 1}
        for tweet in self.__collection.find({},query):
            result.append(list(tweet.values())[0])
        return list(set(result))





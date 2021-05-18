from pymongo import MongoClient
from bson.objectid import ObjectId


def main():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.hatemap
    collection = db.tweets
    post = {'author': 'Sofia',
            'tweet': 'test1'}

    post_id = collection.insert_one(post).inserted_id
    post_id


if __name__ == "__main__":
    main()
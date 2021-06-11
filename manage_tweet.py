import logging
from datetime import time, datetime
import time

import yaml

from DataBase import DataBase
from TwitterSearch import TwitterSearch


def main():
    global db, query
    with open("manage_config.yml", "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        mode = cfg['mode']
        sentiment = cfg['criteria']['sentiment']
        keywords = cfg['criteria']['keywords']
        if keywords:
            keywords = keywords.split(",")
        postag = cfg['criteria']['postag']
        raw_query = cfg['criteria']['raw_query']

    logging.basicConfig()
    log = logging.getLogger("MANAGE")
    log.setLevel(logging.INFO)

    if mode == 'delete':
        log.info("MODE: DELETE")

        db = DataBase('manage_config.yml')
        query = {}
        if sentiment:
            query = {"$or": [{'sentiment.sent-it.sentiment': sentiment}, {'sentiment.feel-it.sentiment': sentiment}]}
        elif keywords:
            _and = []
            for k in keywords:
                _and.append({"spacy.processed_text": {"$regex": ".*{}.*".format(k.strip()), "$options": "i"}})

            query["$and"] = _and
        elif raw_query:
            query = raw_query
        elif postag:
            query = {"spacy.processed_text": {"$regex": ".* POS : {}.*".format(postag.strip()), "$options": "i"}}

    if query:
        deleted = db.delete_more(query)
        log.info("DELETED: {} TWEETS".format(deleted))
    else:
        log.info("NO TWEETS TO DELETE")

    start = time.time()
    log.info(datetime.fromtimestamp(start))
    end = time.time()
    log.info("DONE IN: {}".format(end - start))


if __name__ == "__main__":
    main()

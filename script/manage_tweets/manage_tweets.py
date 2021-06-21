import logging
import os
from datetime import time
import time
from json import dumps

import pandas
import yaml

from hate_tweet_map.database import DataBase


def main():
    global db, query
    start = time.time()
    logging.basicConfig()

    with open("manage_tweets.config", "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        mode = cfg['mode']
        _format = cfg['format']
        sentiment = cfg['criteria']['sentiment']
        keywords_path = cfg['criteria']['keywords']['path']
        keywords_words = cfg['criteria']['keywords']['words']
        _words = []
        logical_operator = cfg['criteria']['logical_operator']
        postag = cfg['criteria']['postag']
        raw_query = cfg['criteria']['raw_query']

    if sentiment is None and keywords_words and None and postag is None and raw_query is None:
        raise ValueError("Please specify at least one value for the criteria field")

    if keywords_path is None and keywords_words is None:
        raise ValueError("It's not possible set the words and the path for the keywords field .")

    if keywords_path:
        with open(keywords_path, "r") as f:
            _words = f.readlines()
    elif keywords_words:
        _words = keywords_words.split(",")

    if mode != "extract" and mode != "delete":
        raise ValueError("The only possible modes are: extract, delete")
    if mode == "extract":
        if _format is None:
            raise ValueError("If you want extract the tweets please specify the format. The possible formats are: "
                             "json, csv")
        elif _format != "json" and _format != "csv":
            raise ValueError("The only possible formats are: csv, json")

    log = logging.getLogger("MANAGE")
    log.setLevel(logging.INFO)

    db = DataBase('manage_tweets.config')
    values = []
    if logical_operator == "and":
        query = {"$and": values}
    else:
        query = {"$or": values}

    if sentiment:
        values.append({"$or": [{'sentiment.sent-it.sentiment': sentiment}, {'sentiment.feel-it.sentiment': sentiment}]})
    if _words:
        for k in _words:
            values.append({"spacy.processed_text": {"$regex": ".*{}.*".format(k.strip()), "$options": "i"}})
    if raw_query:
        values.append(raw_query)
    if postag:
        values.append({"spacy.processed_text": {"$regex": ".* POS : {}.*".format(postag.strip()), "$options": "i"}})

    if mode == 'delete':
        log.info("MODE: DELETE")
        if query:
            deleted = db.delete_more(query)
            log.info("DELETED: {} TWEETS".format(deleted))
        else:
            log.info("NO TWEETS TO DELETE")
    elif mode == 'extract':
        log.info("MODE: EXTRACT")
        result = db.extract(query)
        log.info("TWEETS RETRIEVED: {}".format(len(result)))
        if _format == "json":
            with open('../../data.json', 'w') as file:
                file.write(dumps(result, indent=2))
                log.info("TWEETS SAVED ON: {}".format(os.path.abspath('../../data.json')))
        elif _format == "csv":
            df = pandas.DataFrame(db.extract(query))
            df.to_csv('data.csv', index=False)
            log.info("TWEETS SAVED ON: {}".format(os.path.abspath('../../data.csv')))

    end = time.time()
    log.info("DONE IN: {}".format(end - start))


if __name__ == "__main__":
    main()

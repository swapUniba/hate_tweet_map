import logging
from datetime import time, datetime
import time
from json import dumps

import pandas
import yaml

from DataBase import DataBase
from TwitterSearch import TwitterSearch


def main():
    global db, query
    start = time.time()
    logging.basicConfig()

    with open("manage_config.yml", "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        mode = cfg['mode']
        _format = cfg['format']
        sentiment = cfg['criteria']['sentiment']
        keywords = cfg['criteria']['keywords']
        if keywords:
            keywords = keywords.split(",")
        postag = cfg['criteria']['postag']
        raw_query = cfg['criteria']['raw_query']

    if sentiment is None or keywords is None or postag is None or raw_query is None:
        raise ValueError("Please specify at least one value for the criteria field")

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

    if mode == 'delete':
        log.info("MODE: DELETE")
        if query:
            deleted = db.delete_more(query)
            log.info("DELETED: {} TWEETS".format(deleted))
        else:
            log.info("NO TWEETS TO DELETE")
    elif mode == 'extract':
        if _format == "json":
            with open('data.json', 'w') as file:
                file.write(dumps(db.extract(query), indent=2))
        elif _format == "csv":
            df = pandas.DataFrame(db.extract(query))
            df.to_csv('data.csv', index=False)
    else:
        raise ValueError("The only possible modes are: extract, delete")

    log.info(datetime.fromtimestamp(start))
    end = time.time()
    log.info("DONE IN: {}".format(end - start))


if __name__ == "__main__":
    main()

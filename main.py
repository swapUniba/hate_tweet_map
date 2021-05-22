import requests
import json
import time
from feel_it import EmotionClassifier, SentimentClassifier

import spacy
from pymongo import MongoClient
from yaml import BaseLoader

import MyTagMe

import yaml

from EntityLinker import EntityLinker
from TwitterSearch import TwitterSearch


class DataBase:

    def __init__(self):
        with open("config.yml", "r") as yamlfile:
            cfg = yaml.load(yamlfile, Loader=BaseLoader)

            self.__mongo_db_url = cfg['mongodb']['url']
            self.__mongo_db_database_name = cfg['mongodb']['database']
            self.__mongo_db_collection_name = cfg['mongodb']['collection']

    def delete_tweets_already_saved(self, twitter_results=[]):
        client = MongoClient(self.__mongo_db_url)
        db = client.get_database(self.__mongo_db_database_name)
        collection = db.get_collection(self.__mongo_db_collection_name)
        for response in twitter_results:
            for tweet in response['data']:
                if collection.count_documents({"_id": tweet['id']}) > 0:
                    response['data'].remove(tweet)
        return twitter_results

    def save(self, tweets=[]):
        client = MongoClient(self.__mongo_db_url)
        db = client.get_database(self.__mongo_db_database_name)
        collection = db.get_collection(self.__mongo_db_collection_name)
        collection.insert_many(tweets)


def main():
    twitter_search = TwitterSearch()
    twitter_results = twitter_search.search()
    mongo_db = DataBase()
    twitter_results = mongo_db.delete_tweets_already_saved(twitter_results)
    pre_processed_tweets = pre_process_response(twitter_results)
    tag_me = EntityLinker()
    for t in pre_processed_tweets:
        text = t['raw_text']
        spacy_processed_text, spacy_entities = spacy_process(text)
        t['spacy_processed_text'] = spacy_processed_text
        t['spacy_entities'] = spacy_entities
        emotion_classifier = EmotionClassifier()
        sentiment_classifier = SentimentClassifier()
        hold_list = [text]
        sentiment_analyses = {'emotion': emotion_classifier.predict(hold_list),
                              'sentiment': sentiment_classifier.predict(hold_list)}

        t['sentiment'] = sentiment_analyses
        t['tags'] = tag_me.tag(text)
    mongo_db.save(pre_processed_tweets)


def pre_process_response(twitter_results=[]):
    tweets_processed = []
    for tweets in twitter_results:
        for t in tweets['data']:
            post = {'_id': t['id'], 'author_id': t['id'], 'raw_text': t['text']}
            if 'referenced_tweets' in t:
                for rft in t['referenced_tweets']:
                    if rft['type'] == 'retweeted':
                        post['referenced_tweet'] = rft['id']
                        for p in tweets['includes']['tweets']:
                            if p['id'] == post['referenced_tweet']:
                                post['raw_text'] = p['text']
                                break
                        break

            post['metrics'] = t['public_metrics']
            if 'entities' in t:
                if 'hashtag' in t['entities']:
                    hashtags = ""
                    for hashtag in t['entities']['hashtags']:
                        hashtags += " " + hashtag['tag']
                    post['hashtags'] = hashtags

                if 'mentions' in t['entities']:
                    mentions = ""
                    for mention in t['entities']['mentions']:
                        mentions += " " + mention['username']
                    post['mentions'] = mentions

                if 'urls' in t['entities']:
                    urls = ""
                    for url in t['entities']['urls']:
                        urls += " " + url['url']
                    post['urls'] = urls

            if 'context_annotations' in t:
                post['twitter_context_annotations'] = t['context_annotations']
            if 'geo' in t:
                post['geo_id'] = t['geo']['place_id']
                for p in tweets['includes']['places']:
                    if p['id'] == post['geo_id']:
                        post['country'] = p['country']
                        post['city'] = p['full_name']
                        break
            tweets_processed.append(post)
    return tweets_processed


def spacy_process(tweet):
    nlp = spacy.load("it_core_news_lg")
    doc = nlp(tweet)
    customize_stop_words = [
        'no',
        'non',
        'Non',
        'No'
    ]

    for w in customize_stop_words:
        nlp.vocab[w].is_stop = False

    lemmas_with_postag = []
    filtered_sentence = []
    for word in doc:
        lexeme = nlp.vocab[word.lemma_]
        if not lexeme.is_stop and not lexeme.is_space and not lexeme.is_punct:
            filtered_sentence.append(word)

    for token in filtered_sentence:
        lemmas_with_postag.append(token.lemma_ + " POS : " + token.pos_ + " MORPH : " + token.morph.__str__())

    entities = []

    for ent in doc.ents:
        entities.append(ent.text + " : " + ent.label_)

    return lemmas_with_postag, entities


if __name__ == "__main__":
    main()

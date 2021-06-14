import concurrent
from concurrent.futures import ThreadPoolExecutor, Future, as_completed

import geocoder
import requests
import yaml
from feel_it import EmotionClassifier, SentimentClassifier
import spacy

from DataBase import DataBase
from EntityLinker import EntityLinker
import time
from tqdm import tqdm
import logging


class Process:

    def __init__(self):
        self.all_tweets = False
        self.feel_it = False
        self.nlp = False
        self.nlp_module = None
        self.sent_it = False
        self.geo = False
        self.tag_me = False
        self.emotion_classifier = None
        self.sentiment_classifier = None
        # self.stopwords = None
        # with open('stopwords.txt', 'r') as f:
        #     self.stopwords = f.readlines()
        self.log = logging.getLogger('TWEETS PROCESSOR')
        self.log.setLevel(logging.INFO)
        self.load_configuration()

    def load_configuration(self):
        with open("process_config.yml", "r") as ymlfile:
            cfg = yaml.safe_load(ymlfile)
            self.nlp = cfg['analyzes']['nlp']
            self.tag_me = cfg['analyzes']['tagme']['enabled']
            self.sent_it = cfg['analyzes']['sentiment_analyze']['sent_it']
            self.feel_it = cfg['analyzes']['sentiment_analyze']['feel_it']
            self.geo = cfg['analyzes']['geocoding']
            self.all_tweets = cfg['analyzes']['analyze_all_tweets']

    def process(self, tweets: [], fun, phase_name):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for tweet in tweets:
                text = tweet['raw_text']
                fut = executor.submit(fun, text, tweet)
                fut.add_done_callback(self.save)
                futures.append(fut)
            for job in tqdm(as_completed(futures), total=len(futures), desc=phase_name, leave=True):
                pass

    def start(self):
        start = time.time()

        self.log.info("RETRIEVING TWEETS TO PROCESS FROM DATABASE")

        # 1. extracting tweet in according to configuration

        mongo_db = DataBase("process_config.yml")

        if self.sent_it:
            if self.all_tweets:
                tweets_to_sentit = mongo_db.extract_all_tweets()
            else:
                tweets_to_sentit = mongo_db.extract_new_tweets_to_sentit()
            if len(tweets_to_sentit) > 0:
                # 2.1 Sent-it analyses:
                self.process(tweets_to_sentit, self.sentit_analyze_sentiment, "SENT-IT PHASE")
            else:
                self.log.info("SENT-IT PHASE: NO TWEETS FOUND TO PROCESS")

        # 2.2 tag analyses:
        if self.tag_me:
            if self.all_tweets:
                tweets_to_tag = mongo_db.extract_all_tweets()
            else:
                tweets_to_tag = mongo_db.extract_new_tweets_to_tag()
            if len(tweets_to_tag) > 0:
                self.process(tweets_to_tag, self.link_entity, "ENTITY LINKING PHASE")
            else:
                self.log.info("ENTITY LINKING PHASE: NO TWEETS FOUND TO SENT TO TAG-ME")

        # 2.3 geocode
        if self.geo:
            if self.all_tweets:
                tweets_to_geo = mongo_db.extract_all_tweets_to_geo()
            else:
                tweets_to_geo = mongo_db.extract_new_tweets_to_geo()
            if len(tweets_to_geo) > 0:
                for tweet in tqdm(tweets_to_geo, desc="GEOCODING PHASE", leave=True):
                    city = tweet['city']
                    country = tweet['country']
                    id, check, result, tweet = self.get_osm_coordinates(city, country, tweet)
                    if id == 5:
                        if check:
                            tweet["coordinates"] = result
                    mongo_db.update_one(tweet)
            else:
                self.log.info("GEOCODING PHASE: NO TWEETS FOUND TO GEOCODE")
        # 2.4 feel-it
        if self.feel_it:
            if self.all_tweets:
                tweets_to_feel_it = mongo_db.extract_all_tweets()
            else:
                tweets_to_feel_it = mongo_db.extract_new_tweets_to_feel_it()
            if len(tweets_to_feel_it) > 0:
                self.log.info("FEEL-IT PHASE: LOADING NECESSARY MODULES")
                self.emotion_classifier = EmotionClassifier()
                self.sentiment_classifier = SentimentClassifier()
                # 2.5 feel-it
                for tweet in tqdm(tweets_to_feel_it, desc="FEEL-IT PHASE", leave=True):
                    tweet_text = tweet['raw_text']
                    id, result, tweet = self.feel_it_analyze_sentiment(tweet_text, tweet)
                    if id == 3:
                        if 'sentiment' in tweet:
                            tweet['sentiment']['feel-it'] = result
                        else:
                            tweet['sentiment'] = {}
                            tweet['sentiment']['feel-it'] = result
                    mongo_db.update_one(tweet)
            else:
                self.log.info("FEEL-IT PHASE: NO TWEETS FOUND TO PROCESS")

        # 2.5 nlp analyses:
        if self.nlp:
            if self.all_tweets:
                tweets_to_nlp = mongo_db.extract_all_tweets()
            else:
                tweets_to_nlp = mongo_db.extract_new_tweets_to_nlp()
            if len(tweets_to_nlp) > 0:
                self.nlp_module = spacy.load('it_core_news_lg')
                self.process(tweets_to_nlp, self.process_text_with_spacy, "SPACY PHASE")
            else:
                self.log.info("SPACY PHASE: NO TWEETS FOUND TO PROCESS")

        end = time.time()
        self.log.info("DONE IN: {}".format(end - start))


    def save(self, fut: Future):
        process_id, result, tweet = fut.result()
        if process_id == 2:
            if 'sentiment' in tweet:
                tweet['sentiment']['sent-it'] = result
            else:
                tweet['sentiment'] = {}
                tweet['sentiment']['sent-it'] = result
        elif process_id == 4:
            # for s in self.stopwords:
            #     for word in result['processed_text']:
            #         if s in word:
            #             mongo_db = DataBase("process_config.yml")
            #             mongo_db.delete_one(tweet['_id'])
            #             return
            tweet['spacy'] = result
            tweet['processed'] = True
        elif process_id == 1:
            tweet['tags'] = result
        mongo_db = DataBase("process_config.yml")
        mongo_db.update_one(tweet)

    def link_entity(self, tweet_text: "", tweet: {}):
        tag_me = EntityLinker()
        t = {'tag_me': tag_me.tag(tweet_text)}
        return 1, t, tweet

    def sentit_analyze_sentiment(self, tweet_text: "", tweet: {}):
        data = "{\"texts\": [{\"id\": \"1\", \"text\": \""
        data += tweet_text.replace("\n", "").replace("\"", "").replace("\r", "") + "\"}]}"
        url = "http://193.204.187.210:9009/sentipolc/v1/classify"
        json_response = requests.post(url, data=data.encode('utf-8')).json()
        if 'results' in json_response:
            if json_response['results'][0]['polarity'] == "neg":
                polarity = "negative"
            elif json_response['results'][0]['polarity'] == "pos":
                polarity = "positive"
            else:
                polarity = "neutral"
            sentiment_analyses = {'subjectivity': json_response['results'][0]['subjectivity'],
                                  'sentiment': polarity}

            return 2, sentiment_analyses, tweet
        return 2, {}, tweet

    def feel_it_analyze_sentiment(self, tweet_text: "", tweet: {}):
        hold_list = [tweet_text]
        try:
            sentiment_analyses: dict[str, str] = {'emotion': self.emotion_classifier.predict(hold_list)[0],
                                                  'sentiment': self.sentiment_classifier.predict(hold_list)[0]}
        except:
            time.sleep(0.01)
            return self.feel_it_analyze_sentiment(tweet)

        return 3, sentiment_analyses, tweet

    def process_text_with_spacy(self, text_tweet: "", tweet: {}):
        doc = self.nlp_module(text_tweet)
        customize_stop_words = [
            'no',
            'non',
            'Non',
            'No'
        ]

        for w in customize_stop_words:
            self.nlp_module.vocab[w].is_stop = False

        lemmas_with_postag = []
        filtered_sentence = []
        for word in doc:
            lexeme = self.nlp_module.vocab[word.lemma_]
            if not lexeme.is_stop and not lexeme.is_space and not lexeme.is_punct:
                filtered_sentence.append(word)

        for token in filtered_sentence:
            lemmas_with_postag.append(token.lemma_ + " POS : " + token.pos_ + " MORPH : " + token.morph.__str__())

        entities = []

        for ent in doc.ents:
            entities.append(ent.text + " : " + ent.label_)

        return 4, {'processed_text': lemmas_with_postag, 'entities': entities}, tweet

    def get_osm_coordinates(self, city: "", country: "", tweet: {}):
        try:
            g = geocoder.osm(city + "," + country)
            if g.ok:
                return 5, True, {'latitude': g.osm['y'], 'longitude': g.osm['x']}, tweet
            else:
                return 5, False, {}, tweet
        except Exception as e:
            return self.get_osm_coordinates(city, country, tweet)


def main():
    logging.info("CONFIGURING...")
    p = Process()
    p.start()


if __name__ == "__main__":
    main()

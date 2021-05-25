import concurrent
from concurrent.futures import ThreadPoolExecutor, Future, as_completed

import geocoder
import requests
import yaml
from feel_it import EmotionClassifier, SentimentClassifier
import spacy
from yaml import BaseLoader

from DataBase import DataBase
from EntityLinker import EntityLinker
import time
from tqdm import tqdm


class Process:

    def __init__(self):
        self.todo_parallel = []
        self.all_tweets = False
        self.todo_after = []
        self.feel_it = False
        self.nlp = False
        self.load_configuration()
        if self.nlp:
            self.nlp = spacy.load('it_core_news_lg')
        if self.feel_it:
            self.emotion_classifier = EmotionClassifier()
            self.sentiment_classifier = SentimentClassifier()

    def load_configuration(self):
        with open("process_config.yml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=BaseLoader)
            if cfg['analyzes']['nlp'] == 'True':
                self.todo_parallel.append(self.process_text_with_spacy)
                self.nlp = True
            if cfg['analyzes']['tagme']['enabled'] == 'True':
                self.todo_parallel.append(self.link_entity)
            if cfg['analyzes']['sentiment_analyze']['sent_it'] == 'True':
                self.todo_parallel.append(self.sentit_analyze_sentiment)
            if cfg['analyzes']['sentiment_analyze']['feel_it'] == 'True':
                self.todo_after.append(self.feel_it_analyze_sentiment)
                self.feel_it = True
            if cfg['analyzes']['geocoding'] == 'True':
                self.todo_after.append(self.get_osm_coordinates)
            if cfg['analyzes']['analyze_all_tweets'] == 'True':
                self.all_tweets = True

    def start(self):
        start = time.time()


        print("[2/4] retrieving tweets to process from  database...")

        mongo_db = DataBase()
        if self.all_tweets:
            tweets_to_process = mongo_db.extract_all_tweets()
        else:
            tweets_to_process = mongo_db.extract_tweets_not_processed()

        # print("[3/4] instantiating necessary modules...")

        print("[4/4] processing tweets...")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for tweet in tweets_to_process:
                fut = executor.submit(self.process, tweet)
                fut.add_done_callback(self.finalize_process)
                futures.append(fut)
            for job in tqdm(as_completed(futures), total=len(futures)):
                pass

        for tweet in tqdm(tweets_to_process):
            t = mongo_db.find_by_id(tweet['_id'])
            results = []
            for an in self.todo_after:
                results.append(an(tweet))
                # time.sleep(0.8)
            for result in results:
                if 3 in result:
                    if 'sentiment' in tweet:
                        t['sentiment']['feel-it'] = result[1]
                    else:
                        t['sentiment'] = {}
                        t['sentiment']['feel-it'] = result[1]
                elif 5 in result:
                    if True in result:
                        t["coordinates"] = result[2]
            mongo_db.update_one(tweet)

        end = time.time()
        print("done in: {}".format(end - start))

    def process(self, tweet: {}):
        results = []
        text = tweet['raw_text']
        for p in self.todo_parallel:
            results.append(p(text))
        return tweet, results

    def finalize_process(self, fut: Future):
        tweet, results = fut.result()
        for result in results:
            if 4 in result:
                tweet['spacy'] = result[1]
                tweet['processed'] = str(True)
            elif 1 in result:
                tweet['tags'] = result[1]
            elif 2 in result:
                if 'sentiment' in tweet:
                    tweet['sentiment']['sent-it'] = result[1]
                else:
                    tweet['sentiment'] = {}
                    tweet['sentiment']['sent-it'] = result[1]

        mongo_db = DataBase()
        mongo_db.update_one(tweet)

    def link_entity(self, tweet: ""):
        tag_me = EntityLinker()
        t = {'tag_me': tag_me.tag(tweet)}
        return 1, t

    def sentit_analyze_sentiment(self, tweet: ""):
        data = "{\"texts\": [{\"id\": \"1\", \"text\": \""
        data += tweet.replace("\n", "").replace("\"", "").replace("\r", "") + "\"}]}"
        url = "http://193.204.187.210:9009/sentipolc/v1/classify"
        json_response = requests.post(url, data=data.encode('utf-8')).json()
        if 'results' in json_response:
            sentiment_analyses = {'subjectivity': json_response['results'][0]['subjectivity'],
                                  'polarity': json_response['results'][0]['polarity']}
            d = {'sentiment': sentiment_analyses}

            return 2, d
        return 2, {}

    def feel_it_analyze_sentiment(self, tweet: {}):
        hold_list = [tweet['raw_text']]
        try:
            sentiment_analyses: dict[str, str] = {'emotion': self.emotion_classifier.predict(hold_list)[0],
                                                  'sentiment': self.sentiment_classifier.predict(hold_list)[0]}
            d = {'sentiment': sentiment_analyses}
        except:
            time.sleep(0.01)
            return 3, self.feel_it_analyze_sentiment(tweet)

        return 3, d

    def process_text_with_spacy(self, tweet: ""):
        doc = self.nlp(tweet)
        customize_stop_words = [
            'no',
            'non',
            'Non',
            'No'
        ]

        for w in customize_stop_words:
            self.nlp.vocab[w].is_stop = False

        lemmas_with_postag = []
        filtered_sentence = []
        for word in doc:
            lexeme = self.nlp.vocab[word.lemma_]
            if not lexeme.is_stop and not lexeme.is_space and not lexeme.is_punct:
                filtered_sentence.append(word)

        for token in filtered_sentence:
            lemmas_with_postag.append(token.lemma_ + " POS : " + token.pos_ + " MORPH : " + token.morph.__str__())

        entities = []

        for ent in doc.ents:
            entities.append(ent.text + " : " + ent.label_)

        return 4, {'processed_text': lemmas_with_postag, 'entities': entities}

    def get_osm_coordinates(self, tweet: {}):
        if 'city' in tweet and 'country' in tweet:

            try:
                g = geocoder.osm(tweet['city'] + "," + tweet['country'])
                if g.ok:
                    return 5, True, {'latitude': g.osm['y'], 'longitude': g.osm['x']}
                else:
                    return 5, False, "", ""
            except Exception as e:
                return self.get_osm_coordinates(tweet)
        else:
            return 5, False, "", ""


def main():
    print("[1/4] configuring...")
    p = Process()
    p.start()


if __name__ == "__main__":
    main()

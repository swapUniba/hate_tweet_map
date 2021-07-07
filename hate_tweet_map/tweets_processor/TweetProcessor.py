import concurrent
import os
from concurrent.futures import ThreadPoolExecutor, Future, as_completed
from typing import Optional, List, Tuple

import geocoder
import requests
import urllib3.exceptions
import yaml
from feel_it import EmotionClassifier, SentimentClassifier
import spacy

from hate_tweet_map.database import DataBase
from hate_tweet_map.tweets_processor.EntityLinker import EntityLinker
import time
from tqdm import tqdm
import logging


class ProcessTweet:
    """

    """

    def __init__(self, path_to_cnfg_file):
        self.all_tweets = False
        self.feel_it = False
        self.nlp = False
        self.nlp_module = None
        self.sent_it = False
        self.geo = False
        self.tag_me = False
        self.emotion_classifier = None
        self.sentiment_classifier = None
        self.log = logging.getLogger('TWEETS PROCESSOR')
        self.log.setLevel(logging.INFO)
        self.cnfg_file_path = path_to_cnfg_file
        self.mongo_db = None
        self.__load_configuration()

    def __load_configuration(self):
        with open(self.cnfg_file_path, "r") as ymlfile:
            cfg = yaml.safe_load(ymlfile)
            self.nlp = cfg['analyzes']['nlp']
            self.tag_me = cfg['analyzes']['tagme']['enabled']
            self.sent_it = cfg['analyzes']['sentiment_analyze']['sent_it']
            self.feel_it = cfg['analyzes']['sentiment_analyze']['feel_it']
            self.geo = cfg['analyzes']['geocoding']
            self.all_tweets = cfg['analyzes']['analyze_all_tweets']

        self.mongo_db = DataBase(self.cnfg_file_path)

    def __process(self, tweets: list, fun: callable, phase_name: str, id=0):
        # use the multithread to start the same analyss in parallel on more tweets
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            if id == 2:
                total = 0
                for l in tweets:
                    total = total + len(l)
                    fut = executor.submit(fun, l)
                    # when finish the analysis on the tweet save the result
                    fut.add_done_callback(self.__save)
                    futures.append(fut)
                bar = tqdm(futures, total=total, desc=phase_name, leave=True)
                for job in as_completed(futures):
                    bar.update(100)
            else:
                # for each tweet given
                for tweet in tweets:
                    # retrieve the text of the tweet
                    text = tweet['raw_text']
                    # submit the function, so the analysis to perfonrm on the tweet, and pass to it the tweet and the text of the tweet
                    fut = executor.submit(fun, text, tweet)
                    # when finish the analysis on the tweet save the result
                    fut.add_done_callback(self.__save)
                    futures.append(fut)
                # wait that all tweets have been processed
                for job in tqdm(as_completed(futures), total=len(futures), desc=phase_name, leave=True):
                    pass

    def start(self):
        """
        This method start the process on the tweets in according with the configuyration.
        For easch phase enabled in the config file the method retrieve the tweets to analyze,
        do the analyses and save all tweets process on the database.
        So after each phase the tweets processed are updated in the db.
        When the field all_tweets is set to False in the config file for each phase are retrieved from the database
        the tweets were the processed field is False and that have not already been processed by that phase
        (eg. for sentiment analyses that have not the field sentiment  or for geo that have not the field geo.coordinates).
        Instead if the value of all_tweets is True all the tweets in the db are processed.
        :return: None
        """
        start = time.time()

        self.log.info("RETRIEVING TWEETS TO PROCESS FROM DATABASE")

        # connect to the db indicate on the config file

        # if the sent_it analysis have to be done
        if self.sent_it:
            if self.check_sent_it_availability():
                # if must be analyzed all tweets in the db
                if self.all_tweets:
                    # extract all tweets from the db
                    tweets_to_sentit = self.mongo_db.extract_all_tweets()
                else:
                    # if not all tweets have to be analyzed, ectract from the db only the tweets that
                    # have not yet the field sentiment.sent-it and that are not already processed by spacy.
                    tweets_to_sentit = self.mongo_db.extract_new_tweets_to_sentit()
                if len(tweets_to_sentit) > 0:
                    # 2.1 Sent-it analyses: send all tweets extracted to process function, so pass the list of the
                    # tweets, the function to apply on the tweets, sent_it, and the name of the phase.
                    # N.B process save the result of the analyses on the db
                    # self.__process(tweets_to_sentit, self.__sent_it_analyze_sentiment, "SENT-IT PHASE")
                    to_send_per_time = list(self.divide_chunks(tweets_to_sentit, 100))
                    self.__process(to_send_per_time, self.__sent_it_analyze_sentiment2, "SENT-IT PHASE", 2)

                else:
                    self.log.info("SENT-IT PHASE: NO TWEETS FOUND TO PROCESS")

        # if the entity linker analysis have to be done
        if self.tag_me:
            # if must be analyzed all tweets in the db
            if self.all_tweets:
                # extract all tweets from the db
                tweets_to_tag = self.mongo_db.extract_all_tweets()
            else:
                # if not all tweets have to be analyzed, ectract from the db only the tweets that
                # have not yet the field tags.tag_me and that are not already processed by spacy.
                tweets_to_tag = self.mongo_db.extract_new_tweets_to_tag()
            if len(tweets_to_tag) > 0:
                # 2.2 tag analyses: send all tweets extracted to process function, so pass the list of the
                # tweets, the function to apply on the tweets, link_entity, and the name of the phase.
                # N.B process save the result of the analyses on the db
                self.__process(tweets_to_tag, self.__link_entity, "ENTITY LINKING PHASE")
            else:
                self.log.info("ENTITY LINKING PHASE: NO TWEETS FOUND TO SENT TO TAG-ME")

        # 2.3 geocode
        # if the geo code analysis have to be done
        if self.geo:
            # if must be analyzed all tweets in the db extract from it all tweets
            # that have the field geo.user_location or the field geo.city, geo.country
            if self.all_tweets:
                tweets_to_geo = self.mongo_db.extract_all_tweets_to_geo()
            else:
                # if not all tweets have to be analyzed, extract from the db only the tweets that have are not been
                # processed by spacy and have not yet the field geo.coordinates and have or the fields geo.city,
                # geo.country or have the field geo.user_location
                tweets_to_geo = self.mongo_db.extract_new_tweets_to_geo()
            if len(tweets_to_geo) > 0:
                for tweet in tqdm(tweets_to_geo, desc="GEOCODING PHASE", leave=True):
                    # extracts the information from the tweet
                    usr_location, city, country = None, None, None
                    if "user_location" in tweet["geo"]:
                        usr_location = tweet["geo"]["user_location"]
                    else:
                        city = tweet.get("geo").get('city')
                        country = tweet.get("geo").get('country')
                    # find the coordinates
                    id, check, result, tweet = self.__get_osm_coordinates(tweet=tweet, user_location=usr_location,
                                                                          city=city, country=country)
                    # save the result
                    if id == 5:
                        if check:
                            tweet["geo"]["coordinates"] = result
                    self.mongo_db.update_one(tweet)
            else:
                self.log.info("GEOCODING PHASE: NO TWEETS FOUND TO GEOCODE")

        # if the feel it sentiment analysis have to be done
        if self.feel_it:
            # if must be analyzed all tweets in the db extract from it all tweets
            # in italian language
            if self.all_tweets:
                tweets_to_feel_it = self.mongo_db.extract_all_tweets_to_feel_it()
            # if not all tweets have to be analyzed, extract from the db only the tweets that have are not been
            # processed by spacy and that are in italian language
            else:
                tweets_to_feel_it = self.mongo_db.extract_new_tweets_to_feel_it()
            if len(tweets_to_feel_it) > 0:
                self.log.info("FEEL-IT PHASE: LOADING NECESSARY MODULES")
                self.emotion_classifier = EmotionClassifier()
                self.sentiment_classifier = SentimentClassifier()
                # 2.5 feel-it
                # for each tweet
                for tweet in tqdm(tweets_to_feel_it, desc="FEEL-IT PHASE", leave=True):
                    # extract the text of the tweet
                    tweet_text = tweet['raw_text']
                    # analyzd the tweet with feel-it module
                    id, result, tweet = self.__feel_it_analyze_sentiment(tweet_text, tweet)
                    # save the result
                    if id == 3:
                        # if a ssentiment analysis are yet done, adds the result of fee-it to it
                        if 'sentiment' in tweet:
                            tweet['sentiment']['feel-it'] = result
                        # else create the field sentiment, add the field feel-it and save the result of the analysis
                        else:
                            tweet['sentiment'] = {}
                            tweet['sentiment']['feel-it'] = result
                    self.mongo_db.update_one(tweet)
            else:
                self.log.info("FEEL-IT PHASE: NO TWEETS FOUND TO PROCESS")

        # 2.5 nlp analyses:
        # if the nlp analysis with spacy have to be done
        if self.nlp:
            # if must be analyzed all tweets in the db extract from it all tweets
            if self.all_tweets:
                tweets_to_nlp = self.mongo_db.extract_all_tweets()
            # else extract only the tweets not yet processed by spacy
            else:
                tweets_to_nlp = self.mongo_db.extract_new_tweets_to_nlp()
            if len(tweets_to_nlp) > 0:
                # separate the italian tweets from the english tweet
                ita_tweets_to_nlp = [t for t in tweets_to_nlp if t['lang'] == 'it']
                eng_tweets_to_nlp = [t for t in tweets_to_nlp if t['lang'] == 'en']
                if len(ita_tweets_to_nlp) > 0:
                    # load the italian spacy model
                    self.log.info("SPACY PHASE: LOADING ITA MODEL")
                    self.nlp_module = spacy.load('it_core_news_lg')
                    # send all tweets extracted to process function, so pass the list of the italian
                    # tweets, the function to apply on the tweets, process_text_with_spacy, and the name of the phase.
                    # N.B process save the result of the analyses on the db
                    self.__process(ita_tweets_to_nlp, self.__process_text_with_spacy, "SPACY PHASE:IT")
                if len(eng_tweets_to_nlp) > 0:
                    # load the english spacy model
                    self.log.info("SPACY PHASE: LOADING ENG MODEL")
                    self.nlp_module = spacy.load('en_core_web_lg')
                    # send all tweets extracted to process function, so pass the list of the english
                    # tweets, the function to apply on the tweets, process_text_with_spacy, and the name of the phase.
                    # N.B process save the result of the analyses on the db
                    self.__process(eng_tweets_to_nlp, self.__process_text_with_spacy, "SPACY PHASE:ENG")
            else:
                self.log.info("SPACY PHASE: NO TWEETS FOUND TO PROCESS")

        end = time.time()
        self.log.info("DONE IN: {}".format(end - start))

    def divide_chunks(self, l, n):

        # looping till length l
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def __save(self, fut: Future):
        """
        This is the callback function. when a tweets finish to be processed in it's thread
        this function retrieve the result returned by the function called by the thread, unpack it,
        adds the information on the tweet and save it in the db.

        :param fut: the future object that contains the transformation done on the tweet
        :type fut: Future
        :return: None
        """

        process_id, result, tweet = fut.result()
        # save the result in the right field in according to the process id returned
        if process_id == 2:
            for r in result:
                for t in tweet:
                    if r["id"] == t["_id"]:
                        if r['polarity'] == "neg":
                            r['polarity'] = "negative"
                        elif r['polarity'] == "pos":
                            r['polarity'] = "positive"
                        if 'sentiment' in t:
                            t['sentiment']['sent-it'] = {"subjectivity": r["subjectivity"], "sentiment": r["polarity"]}
                        else:
                            t['sentiment'] = {}
                            t['sentiment']['sent-it'] = {"subjectivity": r["subjectivity"],
                                                                                     "sentiment": r["polarity"]}
                        self.mongo_db.update_one(t)
                        break
            return
        elif process_id == 4:
            tweet['spacy'] = result
            tweet['processed'] = True
        elif process_id == 1:
            tweet['tags'] = result

        # save the tweet on the db
        self.mongo_db.update_one(tweet)

    def __link_entity(self, tweet_text: str, tweet: dict) -> Tuple[int, dict, dict]:
        """
        This method use the sent-it uniba service to perform the sentiment analyses of the tweet.

        :param tweet_text: the text of the tweet
        :type tweet_text: str
        :param tweet: a dictionary representing the tweet
        :type tweet: dict
        :return: the id of the process:1; a dictionary representing the result of the analyses; a dictionary representing the original tweet.
        :rtype: Tuple[int, dict, dict]
        """
        # create an EntityLinker object
        tag_me = EntityLinker(self.cnfg_file_path)
        # connect to the service and save the result in a dict t
        t = {'tag_me': tag_me.tag(tweet_text, tweet['lang'])}
        # return the process id (1), the result (the dict t), and the tweet analyzed
        return 1, t, tweet

    def check_sent_it_availability(self) -> bool:
        data = "{\"texts\": [{\"id\": \"1\", \"text\":\"Please vote for our nation's group and South Korea's pride, BTS. https://t.co/MsvLwepLRj \"}]}"
        url = "http://193.204.187.210:9009/sentipolc/v1/classify"
        try:
            json_response = requests.post(url, data=data.encode('utf-8')).json()
            if 'results' in json_response:
                return True
            else:
                return False
        except requests.exceptions.ConnectionError or urllib3.exceptions.MaxRetryError \
               or urllib3.exceptions.NewConnectionError or ConnectionRefusedError as e:
            self.log.warning("SENT-IT PHASE:IMPOSSIBLE TO ESTABLISH CONNECTION WITH SENT-IT SERVICE. PHASE SKIPPED.")
            return False

    def __sent_it_analyze_sentiment2(self, tweets: list) -> Tuple[int, list, list]:
        """
        This method use the sent-it uniba service to perform the sentiment analyses of the tweet:

        :param tweets: list of tweets to send to sent_it
        :type tweets: list
        :return: the id of the process:2; a list represent the result of the analysis (empty if something goes wrong); a list representing the original tweets.
        :rtype: Tuple[int, list, list]
        """
        # build the request to send to ths server
        self.log.debug('building')
        d = []
        for t in tweets:
            d.append("{\"id\": \"" + str(t["_id"]) + "\", \"text\": \"" + t["raw_text"].replace("\n", "").replace("\"",
                                                                                                                  "").replace(
                "\r", "") + "\"}")

        data = "{\"texts\": [" + ",".join(d) + "]}"
        # remove special charachters from the teof the tweet before send it
        # data += tweet_text.replace("\n", "").replace("\"", "").replace("\r", "") + "\"}]}"
        # set the url
        url = "http://193.204.187.210:9009/sentipolc/v1/classify"
        # send the request and save the response in json
        try:
            self.log.debug('sending')
            json_response = requests.post(url, data=data.encode('utf-8')).json()
            # if there is a result in the response
            if 'results' in json_response:
                return 2, json_response["results"], tweets
            else:
                return 2, [], tweets
        except requests.exceptions.ConnectionError or urllib3.exceptions.MaxRetryError \
               or urllib3.exceptions.NewConnectionError or ConnectionRefusedError as e:
            return 2, [], tweets

    def __sent_it_analyze_sentiment(self, tweet_text: str, tweet: dict) -> Tuple[int, dict, dict]:
        """
        This method use the sent-it uniba service to perform the sentiment analyses of the tweet:

        :param tweet_text: the text of the tweet
        :type tweet_text: str
        :param dict tweet: a dictionary representing the tweet
        :type tweet: dict
        :return: the id of the process:2; a dictionary represent the result of the analysis (empty if something goes wrong); a dictionary representing the original tweet.
        :rtype: Tuple[int, dict, dict]
        """
        # build the request to send to ths server
        data = "{\"texts\": [{\"id\": \"1\", \"text\": \""
        # remove special charachters from the teof the tweet before send it
        data += tweet_text.replace("\n", "").replace("\"", "").replace("\r", "") + "\"}]}"
        # set the url
        url = "http://193.204.187.210:9009/sentipolc/v1/classify"
        # send the request and save the response in json
        try:
            json_response = requests.post(url, data=data.encode('utf-8')).json()
            # if there is a result in the response
            if 'results' in json_response:
                # save the result (for consistence the result is normalized)
                if json_response['results'][0]['polarity'] == "neg":
                    polarity = "negative"
                elif json_response['results'][0]['polarity'] == "pos":
                    polarity = "positive"
                else:
                    polarity = "neutral"
                sentiment_analyses = {'subjectivity': json_response['results'][0]['subjectivity'],
                                      'sentiment': polarity}
                # return the id of the process (2), the result of the analyses, and the original tweet
                return 2, sentiment_analyses, tweet
            else:
                return 2, {}, tweet
        except requests.exceptions.ConnectionError or urllib3.exceptions.MaxRetryError \
               or urllib3.exceptions.NewConnectionError or ConnectionRefusedError as e:
            self.log.warning(
                "\nSENT-IT PHASE:IMPOSSIBLE TO ESTABLISH CONNECTION WITH SENT-IT SERVICE. WAITING AND RETRYING.")
            time.sleep(2)
            return self.__sent_it_analyze_sentiment(tweet_text=tweet_text, tweet=tweet)

    def __feel_it_analyze_sentiment(self, tweet_text: str, tweet: dict) -> Tuple[int, dict, dict]:
        """
        This method use the feel-it algorithms to perform the sentiment and emotion analysis.

        | NB. these models works only with italian language.

        :param tweet_text: the text of the tweet
        :type tweet_text: str
        :param tweet: a dict representing the tweet
        :type tweet: dict
        :return: the id of the process: 3; a dictionary that contains the result of the analysis; the tweet analyzed
        :rtype: Tuple[int, dict, dict]
        """
        # create a list and insert the text of the tweet
        hold_list = [tweet_text]
        try:
            # try to analyze the sentiment of the text with feel-it algorithm and save the result in a dict
            sentiment_analyses: dict[str, str] = {'emotion': self.emotion_classifier.predict(hold_list)[0],
                                                  'sentiment': self.sentiment_classifier.predict(hold_list)[0]}
        except:
            # if the model is busy wait and retry
            time.sleep(0.01)
            return self.__feel_it_analyze_sentiment(tweet)
        # return the process id (3), the result and the tweet
        return 3, sentiment_analyses, tweet

    def __process_text_with_spacy(self, text_tweet: str, tweet: dict) -> Tuple[int, dict, dict]:
        """
        This method perform the natural language processing on the tweet text using spacy.

        :param text_tweet: the text of the tweet
        :type text_tweet: str
        :param tweet: a dict representing the tweet
        :type tweet: dict
        :return: the id of the process: 4; a dictionary that contains the result of the analysis; the tweet analyzed
        :rtype: Tuple[int, dict, dict]
        """
        # perform the analysis of the text with spacy
        doc = self.nlp_module(text_tweet)
        customize_stop_words = [
            'no',
            'non',
            'Non',
            'No'
        ]
        # customize the stopwords
        for w in customize_stop_words:
            self.nlp_module.vocab[w].is_stop = False

        lemmas_with_postag = []
        filtered_sentence = []
        # remove space, punct and stopwords from the tweet text
        for word in doc:
            lexeme = self.nlp_module.vocab[word.lemma_]
            if not lexeme.is_stop and not lexeme.is_space and not lexeme.is_punct:
                filtered_sentence.append(word)

        # for each token remained save the lemma, the pos information adn the morphology
        for token in filtered_sentence:
            lemmas_with_postag.append(token.lemma_ + " POS : " + token.pos_ + " MORPH : " + token.morph.__str__())

        entities = []
        # retrieve the entities recognized from spacy
        for ent in doc.ents:
            entities.append(ent.text + " : " + ent.label_)

        return 4, {'processed_text': lemmas_with_postag, 'entities': entities}, tweet

    def __get_osm_coordinates(self, tweet: dict, user_location: Optional[str], city: Optional[str],
                              country: Optional[str]) \
            -> Tuple[int, bool, dict, dict]:
        """
        This method use the Open Street Map service to find the coordinates of a specific location.

        :param tweet: the tweet analyzed
        :type tweet: dict
        :param user_location: the user_location if the tweet contains it
        :type user_location: str, optional
        :param city: the city from where the tweet has been posted if the tweet contains it
        :type city: str, optional
        :param country: the country from where the tweet has been posted if the tweet contains it
        :type country: str, optional
        :return: the id of the process: 5; a dictionary that contains the result of the analysis; the tweet analyzed
        :rtype: Tuple[int, bool, dict, dict]
        """

        g = None
        # build the dict to send as request to the osm service withe the information given
        try:
            if user_location is not None:
                g = geocoder.osm(user_location)
            elif city is not None and country is not None:
                g = geocoder.osm(city + "," + country)
        except urllib3.exceptions.ReadTimeoutError or urllib3.exceptions.TimeoutError or urllib3.exceptions.ConnectionError or ConnectionError or TimeoutError:
            time.sleep(0.5)
            self.log.warning("GEO PHASE: ERROR DURING THE CONNECTION. RETRYING.")
            return self.__get_osm_coordinates(tweet, user_location, city, country)
        except ValueError:
            return 5, False, {}, tweet
        # return the coordinates if the result of the request is ok
        if g.ok:
            return 5, True, {'latitude': g.osm['y'], 'longitude': g.osm['x']}, tweet
        # return an empty dict if the result is not ok
        else:
            return 5, False, {}, tweet

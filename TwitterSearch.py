import concurrent
from concurrent import futures
import json
import logging
import math
import time
# from winsound import Beep
from concurrent.futures import Future
from datetime import datetime, timezone

import requests
import yaml
from tqdm import tqdm
from yaml import BaseLoader

import util
from DataBase import DataBase


class TwitterSearch:

    def __init__(self, mongodb: DataBase):
        self.mongodb = mongodb
        self._all = []
        self.total_result = 0
        self.__multi_user = False
        self.__users = []

        self.log = logging.getLogger("SEARCH")
        self.log.setLevel(logging.INFO)
        logging.basicConfig()
        self.response = {}
        with open("search_config.yml", "r") as ymlfile:
            cfg = yaml.safe_load(ymlfile)
            check = []
            self.__twitter_keyword = cfg['twitter']['search']['keyword']
            self.__twitter_user = str(cfg['twitter']['search']['user'])

            if not (self.__twitter_keyword or self.__twitter_user):
                raise ValueError(
                    'Impostare un valore per almeno uno dei due perametri [user], [keyword]')
            if self.__twitter_user:
                if "," in self.__twitter_user:
                    self.__multi_user = True
                    self.__users = self.__twitter_user.split(",")

            self.__twitter_lang = cfg['twitter']['search']['lang']
            self.__twitter_place_country = cfg['twitter']['search']["geo"]['place_country']
            self.__twitter_place = cfg['twitter']['search']["geo"]['place']
            self.__twitter_bounding_box = cfg['twitter']['search']["geo"]['bounding_box']
            self.__twitter_point_radius_longitude = cfg['twitter']['search']["geo"]['point_radius']['longitude']
            self.__twitter_point_radius_latitude = cfg['twitter']['search']["geo"]['point_radius']['latitude']
            self.__twitter_point_radius_radius = cfg['twitter']['search']["geo"]['point_radius']['radius']
            self.__twitter_start_time = cfg['twitter']['search']['time']['start_time']
            self.__twitter_end_time = cfg['twitter']['search']['time']['end_time']

            if self.__twitter_point_radius_longitude:
                check.append(True)
            if self.__twitter_point_radius_radius:
                check.append(True)
            if self.__twitter_point_radius_latitude:
                check.append(True)

            if 1 < check.count(True) < 3:
                raise ValueError(
                    'Per cercare utilizzando [point_radius] tutti i seguenti parametri devono essere inserito [latitude], [radius] e [longitude]')

            check = []

            if self.__twitter_place:
                check.append(True)
            if self.__twitter_place_country:
                check.append(True)
            if self.__twitter_bounding_box:
                check.append(True)
            if self.__twitter_point_radius_longitude:
                check.append(True)

            if check.count(True) > 1:
                raise ValueError(
                    'Solo uno tra i paremetri [bounding_box], [point_radius] e [place_country] può essere impostato')

            self.__twitter_context_annotations = cfg['twitter']['search']['context_annotations']
            self.__twitter_all_tweets = cfg['twitter']['search']['all_tweets']
            self.__twitter_n_results = cfg['twitter']['search']['n_results']
            self.__twitter_barer_token = cfg['twitter']['configuration']['barer_token']
            self.__twitter_end_point = cfg['twitter']['configuration']['end_point']

        self.__headers = {"Authorization": "Bearer {}".format(self.__twitter_barer_token)}

    def __next_page(self, next_token=""):
        if next_token != "":
            self.__query["next_token"] = next_token

    def __build_query(self, user=None):
        # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
        # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
        self.__query = {'query': ""}

        if self.__twitter_keyword:
            self.__query['query'] = str(self.__twitter_keyword)
        if not user:
            if self.__twitter_user:
                if self.__twitter_keyword:
                    self.__query['query'] += " from: " + str(self.__twitter_user)
                else:
                    self.__query['query'] += "from: " + str(self.__twitter_user)
        else:
            if self.__twitter_keyword:
                self.__query['query'] += " from: " + str(user)
            else:
                self.__query['query'] += "from: " + str(user)

        if self.__twitter_lang:
            self.__query['query'] += " lang:" + self.__twitter_lang
        if self.__twitter_place:
            self.__query['query'] += " place:" + self.__twitter_place
        if self.__twitter_place_country:
            self.__query['query'] += " place_country:" + self.__twitter_place_country
        if self.__twitter_n_results:
            if self.__twitter_n_results > 500 or self.__twitter_all_tweets:
                self.__query['max_results'] = str(500)
            else:
                self.__query['max_results'] = str(self.__twitter_n_results)
        elif self.__twitter_all_tweets:
            self.__query['max_results'] = str(500)

        if self.__twitter_bounding_box:
            self.__query['query'] += " bounding_box:" + "[" + self.__twitter_bounding_box + "]"
        elif self.__twitter_point_radius_longitude:
            self.__query['query'] += " point_radius:" + "[" + str(self.__twitter_point_radius_longitude) + " " + str(
                self.__twitter_point_radius_latitude) + " " + self.__twitter_point_radius_radius + "]"
        self.__query['place.fields'] = "contained_within,country,country_code,full_name,geo,id,name,place_type"
        self.__query['expansions'] = 'author_id,geo.place_id,referenced_tweets.id'
        self.__query['tweet.fields'] = 'public_metrics,entities,created_at'
        self.__query['user.fields'] = 'username'

        if self.__twitter_context_annotations:
            self.__query['tweet.fields'] += ',context_annotations'
        if self.__twitter_start_time:
            self.__query['start_time'] = str(self.__twitter_start_time)
        if self.__twitter_end_time:
            self.__query['end_time'] = str(self.__twitter_end_time)

    @property
    def twitter_lang(self):
        return self.__twitter_lang

    @property
    def twitter_place_country(self):
        return self.__twitter_place_country

    @property
    def twitter_point_radius_radius(self):
        return self.__twitter_point_radius_radius

    @property
    def twitter_point_radius_longitude(self):
        return self.__twitter_point_radius_longitude

    @property
    def twitter_point_radius_latitude(self):
        return self.__twitter_point_radius_latitude

    @property
    def twitter_place(self):
        return self.__twitter_place

    @property
    def twitter_start_time(self):
        return self.__twitter_start_time

    @property
    def twitter_end_time(self):
        return self.__twitter_end_time

    @property
    def twitter_bounding_box(self):
        return self.__twitter_bounding_box

    @property
    def twitter_context_annotation(self):
        return self.__twitter_context_annotations

    @property
    def twitter_n_results(self):
        return self.__twitter_n_results

    @property
    def twitter_all_results(self):
        return self.__twitter_all_tweets

    @property
    def twitter_end_point(self):
        return self.__twitter_end_point

    @property
    def twitter_key_word(self):
        return self.__twitter_keyword

    @property
    def twitter_user(self):
        return self.__twitter_user

    def __connect_to_endpoint(self, retried=False):
        response = requests.request("GET", self.__twitter_end_point, headers=self.__headers, params=self.__query)
        if response.status_code == 200:
            t = response.headers.get('date')
            self.log.info("RECEIVED VALID RESPONSE")
            return response.json()
        if response.status_code == 429 and not retried:
            self.log.debug("RETRY")
            time.sleep(1)
            return self.__connect_to_endpoint(retried=True)
        elif response.status_code == 429 and retried:
            #            frequency = 2500  # Set Frequency To 2500 Hertz
            #            duration = 3000  # Set Duration To 1000 ms == 1 second
            #            Beep(frequency, duration)
            self.log.info("RATE LIMITS REACHED: WAITING")
            now = time.time()
            now_date = datetime.fromtimestamp(now, timezone.utc)
            reset = float(response.headers.get("x-rate-limit-reset"))
            reset_date = datetime.fromtimestamp(reset, timezone.utc)
            sec_to_reset = (reset_date - now_date).total_seconds()
            for i in tqdm(range(0, math.floor(sec_to_reset) + 1), desc="WAITING FOR (in sec)", leave=True, position=0):
                time.sleep(1)
            return self.__connect_to_endpoint(retried=True)
        if response.status_code == 503:
            self.log.warning(
                "GET BAD RESPONSE FROM TWITTER: {}: {}. THE SERVICE IS OVERLOADED.".format(response.status_code,
                                                                                           response.text))
            self.log.warning("WAITING FOR 1 MINUTE BEFORE RESEND THE REQUEST")
            for i in tqdm(range(0, 60), desc="WAITING FOR (in sec)", leave=True):
                time.sleep(1)
            self.log.warning("RESENDING THE REQUEST")
            return self.__connect_to_endpoint()
        else:
            self.log.critical("GET BAD RESPONSE FROM TWITTER: {}: {}".format(response.status_code, response.text))
            raise Exception(response.status_code, response.text)

    def __make(self, result_obtained_yet=0):
        self.response = self.__connect_to_endpoint()
        while "meta" in self.response:
            self.log.info("RECEIVED: {} TWEETS".format(self.response['meta']['result_count']))
            self.save()
            self.total_result += self.response['meta']['result_count']
            if "next_token" in self.response['meta']:
                if self.__twitter_n_results:
                    if not self.__twitter_all_tweets:
                        result_obtained_yet += int(self.response['meta']['result_count'])
                        results_to_request = self.__twitter_n_results - result_obtained_yet
                        if results_to_request <= 0:
                            return
                        if results_to_request < 10:
                            results_to_request = 10
                        if results_to_request > 500:
                            results_to_request = 500
                        self.log.info("ASKING FOR: {} TWEETS".format(results_to_request))
                        self.__query['max_results'] = results_to_request
                elif self.__twitter_all_tweets:
                    self.log.info("ASKING FOR NEXT PAGE")
                    self.__query['max_results'] = str(500)

                self.__next_page(next_token=self.response["meta"]["next_token"])
                self.response = self.__connect_to_endpoint()
            else:
                break
        self.log.info("THERE ARE NO OTHER PAGE AVAILABLE. ALL TWEETS REACHED")

    def search(self):
        if self.__multi_user:
            self.log.info("MULTI-USERS SEARCH")
            for us in self.__users:
                self.log.info("SEARCH FOR: {}".format(us))
                self.__build_query(user=us)
                self.__make()
        else:
            self.__build_query()
            self.__make()
        return self.total_result

    def save(self):
        self.log.info("SAVING TWEETS")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for tweet in (self.response['data']):
                if not self.mongodb.is_in(tweet['id']):
                    self.log.setLevel(logging.DEBUG)
                    self.log.debug(tweet)
                    fut = executor.submit(util.pre_process_response, tweet, self.response['includes'])
                    fut.add_done_callback(self.save_)
                    futures.append(fut)
                else:
                    self.total_result -= 1
        self.mongodb.save_many(self._all)
        self._all = []

    def save_(self, fut: Future):
        self._all.append(fut.result())

import concurrent
import os
from concurrent import futures
import logging
import math
import time
from concurrent.futures import Future
from datetime import datetime, timezone

import requests
import yaml
from tqdm import tqdm

from hate_tweet_map import util
from hate_tweet_map.database import DataBase


class UserSearch:

    def __init__(self):

        self.__tot_user_saved = 0
        self._all = []
        self.log = logging.getLogger("SEARCH USERS")
        self.log.setLevel(logging.INFO)
        logging.basicConfig()
        self.response = {}
        self.__query = ""
        working_directory = os.path.abspath(os.path.dirname(__file__))
        cnfg_file_path = os.path.join(working_directory, "search_users.config")
        self.log.info("LOADING CONFIGURATION")
        with open(cnfg_file_path, "r") as ymlfile:
            cfg = yaml.safe_load(ymlfile)
            self.mongodb_users = DataBase(cnfg_file_path, key="mongodb_users")
            self.mongodb_tweets = DataBase(cnfg_file_path, key="mongodb_tweets")
            self.__twitter_barer_token = cfg['twitter']['configuration']['barer_token']
            self.__twitter_end_point = cfg['twitter']['configuration']['end_point']

        self.__headers = {"Authorization": "Bearer {}".format(self.__twitter_barer_token)}
        self.__users_to_search = []

    def retrieve_users_id(self):
        to_search = self.mongodb_tweets.get_users_id()
        self.log.info("LOADED {} USERS ID TO SEARCH".format(len(to_search)))
        self.__users_to_search = [str(id) for id in to_search]

    def __next_page(self, next_token=""):
        if next_token != "":
            self.__query["next_token"] = next_token

    def __build_query(self, user=None):

        self.retrieve_users_id()
        ids = ",".join(self.__users_to_search)
        self.__query = {'ids': ids,
                        "user.fields": "id,name,username,location,entities,"
                                       "public_metrics"}

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
        self.log.info("USERS RECEIVED: {}".format(len(self.response["data"])))
        self.save()
        self.log.info("USERS NOT SAVED BECAUSE ALREADY EXISTENT IN THE DB: {}".format(len(self.response["data"]) - self.__tot_user_saved))
        self.log.info("NEW USERS SAVED: {}".format(self.__tot_user_saved))


    def search(self):
        self.__build_query()
        self.__make()


    def save(self):
        self.log.info("SAVING USER INFO")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for user in (self.response['data']):
                if not self.mongodb_users.is_in(user['id']):
                    self.__tot_user_saved += 1
                    self.log.debug(user)
                    fut = executor.submit(util.pre_process_user_response, user)
                    fut.add_done_callback(self.save_)
                    futures.append(fut)
        self.mongodb_users.save_many(self._all)

    def save_(self, fut: Future):
        self._all.append(fut.result())

def main():
    usr = UserSearch()
    usr.search()


if __name__ == "__main__":
    main()
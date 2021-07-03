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
    """

    """

    def __init__(self, path_to_cnfg_file):
        self.__tot_user_saved = 0
        self._all = []
        self.log = logging.getLogger("SEARCH USERS")
        self.log.setLevel(logging.INFO)
        logging.basicConfig()
        self.response = {}
        self.__query = ""
        # find the configuration file and load the configuration from it
        self.log.info("LOADING CONFIGURATION")
        with open(path_to_cnfg_file, "r") as ymlfile:
            cfg = yaml.safe_load(ymlfile)
            # load the database where sava the user information and the database that contains the tweets
            self.mongodb_users = DataBase(path_to_cnfg_file, key="mongodb_users")
            self.mongodb_tweets = DataBase(path_to_cnfg_file, key="mongodb_tweets")
            self.__twitter_barer_token = cfg['twitter']['configuration']['barer_token']
            self.__twitter_end_point = cfg['twitter']['configuration']['end_point']

        self.__headers = {"Authorization": "Bearer {}".format(self.__twitter_barer_token)}
        self.__users_to_search = []

    def __retrieve_users_id(self) -> None:
        """
        This method retrieve all the id of the tweets from the database, than retrieve the id of the users already
        saved, subtract from the users obtained from the tweets the users already saved and finally save these user's
        ids in a list
        """
        to_search = self.mongodb_tweets.get_users_id()
        saved = self.mongodb_users.get_users()
        to_search = [usr for usr in to_search if usr not in saved]
        self.log.info("LOADED {} USERS ID TO SEARCH".format(len(to_search)))
        self.__users_to_search = [str(id) for id in to_search]

    def __build_query(self, users: str) -> None:
        """
        This method build the query to send to the twitter api.

        :param users: a string that contains all the user's ids to search separated by a comma
        :type users: str
        :return: None
        """
        self.__query = {'ids': users,
                        "user.fields": "id,name,username,location,entities,"
                                       "public_metrics"}

    def __connect_to_endpoint(self, retried=False) -> dict:
        """
        This method sends the request to twitter and return the response.
        The possibles status codes in the twitter response are:
            - 200: ok,in this case the response is a valid response;
            - 429: rate limit exceeded, this means that either more requests were sent per second than allowed or more requests were sent in 15min than allowed. so in this case this method waits 1 second and tries to send the request again,  if twitter still replies with a 429 code, it retrieves from the reply the time when the limit will reset and wait for that time to resubmit the request;
            - others: in this case the method raises an exception

        :param retried: a parameter that indicate if it is the first retry after an error or not, defaults to False
        :type retried: bool, optional
        :raise Exception: when twitter response with not 200 or 429 status code.
        :return: dict that contains the response from twitter
        :rtype: dict
        """
        response = requests.request("GET", self.__twitter_end_point, headers=self.__headers, params=self.__query)
        if response.status_code == 200:
            self.log.info("RECEIVED VALID RESPONSE")
            json_response = response.json()
            if "errors" in json_response:
                self.log.warning("RECEIVED VALID RESPONSE WITH ERRORS")
                ids = []
                for i in json_response["errors"]:
                    ids.append(i["value"])
                self.log.warning("IMPOSSIBLE TO RETRIEVE THE FOLLOWING USERS:{}".format(ids))

            return json_response
        if response.status_code == 429 and not retried:
            self.log.debug("RETRY")
            time.sleep(1)
            return self.__connect_to_endpoint(retried=True)
        elif response.status_code == 429 and retried:
            self.log.info("RATE LIMITS REACHED: WAITING")
            now = time.time()
            now_date = datetime.fromtimestamp(now, timezone.utc)
            reset = float(response.headers.get("x-rate-limit-reset"))
            reset_date = datetime.fromtimestamp(reset, timezone.utc)
            sec_to_reset = (reset_date - now_date).total_seconds()
            for i in tqdm(range(0, math.floor(sec_to_reset) + 1), desc="WAITING FOR (in sec)", leave=True, position=0):
                time.sleep(1)
            return self.__connect_to_endpoint(retried=True)
        else:
            self.log.critical("GET BAD RESPONSE FROM TWITTER: {}: {}".format(response.status_code, response.text))
            raise Exception(response.status_code, response.text)

    def __make(self) -> None:
        """
        This method calls the method that send the request to twitter than elaborates and save the response.

        :return: None
        """
        self.response = self.__connect_to_endpoint()
        if "data" in self.response:
            self.log.info("USERS RECEIVED: {}".format(len(self.response["data"])))
            self.__save()
            self.log.info("USERS NOT SAVED BECAUSE ALREADY IN THE DB: {}".format(
                len(self.response["data"]) - self.__tot_user_saved))
            self.log.info("NEW USERS SAVED: {}".format(self.__tot_user_saved))
        else:
            self.log.info("USERS RECEIVED: 0")

    def search(self) -> None:
        """
        This method search, elaborate and save the users on the database.
        The Twitter Search Users endpoint allow to search for 100 users per request.
        If the users to search are more than 100 the number of users to search are split in subset of 100
        and the relative requests are sent.

        :return: None
        """
        self.__retrieve_users_id()
        if len(self.__users_to_search) <= 0:
            self.log.info("NOTHING TO SEARCH")
            return
        if len(self.__users_to_search) > 100:
            # in case of more request to send we disable the info log to print
            # a bar that shows the progress.
            self.log.setLevel(logging.WARNING)
            # calculate hoy many requests must be send to Twitter
            if len(self.__users_to_search) % 100 != 0:
                n_requests = int(len(self.__users_to_search) / 100) + 1
            else:
                n_requests = int(len(self.__users_to_search) / 100)
            with tqdm(self.__users_to_search, desc="Searching", leave=True, position=0) as bar:
                for i in range(0, n_requests):
                    ids = ",".join(self.__users_to_search[:100])
                    self.__build_query(users=ids)
                    self.__make()
                    self.__users_to_search = self.__users_to_search[100:]
                    bar.update(100)
            self.log.setLevel(logging.INFO)
            self.log.info("NEW USERS SAVED: {}".format(self.__tot_user_saved))
        else:
            ids = ",".join(self.__users_to_search)
            self.__build_query(users=ids)
            self.__make()

    def __save(self) -> None:
        """
        This method process in parallel all the tweets received from one request and save
        all processed tweets in the db.

        :return None
        """

        self.log.info("SAVING USER INFO")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for user in (self.response['data']):
                if not self.mongodb_users.is_in(user['id']):
                    self.__tot_user_saved += 1
                    self.log.debug(user)
                    fut = executor.submit(util.pre_process_user_response, user)
                    fut.add_done_callback(self.__save_)
                    futures.append(fut)
        self.mongodb_users.save_many(self._all)
        self._all.clear()

    def __save_(self, fut: Future):
        self._all.append(fut.result())

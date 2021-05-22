import json
import time
import requests
import yaml
from yaml import BaseLoader


class TwitterSearch:

    def __init__(self):
        self.responses = []
        with open("config.yml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=BaseLoader)

            self.__twitter_keyword = cfg['twitter']['search']['keyword']
            self.__twitter_user = cfg['twitter']['search']['user']
            self.__twitter_lang = cfg['twitter']['search']['lang']
            self.__twitter_place_country = cfg['twitter']['search']['place_country']
            self.__twitter_context_annotations = cfg['twitter']['search']['context_annotations']
            self.__twitter_n_results = cfg['twitter']['search']['n_results']
            self.__twitter_barer_token = cfg['twitter']['configuration']['barer_token']
            self.__twitter_end_point = cfg['twitter']['configuration']['end_point']

        self.__headers = {"Authorization": "Bearer {}".format(self.__twitter_barer_token)}
        self.__make_query()

    def __next_page(self, next_token=""):
        if next_token != "":
            self.__query["next_token"] = next_token

    def __make_query(self):
        # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
        # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
        self.__query = {}
        if self.__twitter_keyword == "" and self.__twitter_user == "":
            return ""
        else:
            if self.__twitter_keyword != "":
                self.__query['query'] = self.__twitter_keyword
            if self.__twitter_user != "":
                self.__query['from'] = self.__twitter_user
            self.__query['query'] += " lang:" + self.__twitter_lang
            # query['place'] = place
            self.__query['query'] += " place_country:" + self.__twitter_place_country
            self.__query['place.fields'] = "contained_within,country,country_code,full_name,geo,id,name,place_type"
            self.__query['expansions'] = 'geo.place_id,referenced_tweets.id'
            self.__query['tweet.fields'] = 'author_id' + ',public_metrics,entities'
            if self.__twitter_context_annotations:
                self.__query['tweet.fields'] += ',context_annotations'
            self.__query['max_results'] = str(self.__twitter_n_results)

    def __connect_to_endpoint(self):
        response = requests.request("GET", self.__twitter_end_point, headers=self.__headers, params=self.__query)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

    def __remake(self, response, result_obtained_yet=0):
        if "meta" in response:
            result_obtained_yet += int(response['meta']['result_count'])
            if result_obtained_yet < int(self.__twitter_n_results):
                if "next_token" in response['meta']:
                    results_to_request = int(self.__twitter_n_results) - result_obtained_yet
                    self.__query['max_results'] = str(results_to_request)
                    time.sleep(0.5)
                    self.__next_page(next_token=response["meta"]["next_token"])
                    json_response = self.__connect_to_endpoint()
                    self.responses.append(json_response)
                    print(json.dumps(json_response, indent=4, sort_keys=True))
                    self.__remake(json_response, result_obtained_yet)

    def search(self):

        json_response = self.__connect_to_endpoint()
        print(json.dumps(json_response, indent=4, sort_keys=True))
        self.responses.append(json_response)
        time.sleep(1)
        self.__remake(json_response)
        return self.responses

import json
import time
import requests
import yaml
from yaml import BaseLoader


class TwitterSearch:

    def get_max_result(self):
        return self.__twitter_n_results

    def __init__(self):
        self.responses = []
        with open("search_config.yml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=BaseLoader)
            check = []
            self.__twitter_keyword = str(cfg['twitter']['search']['keyword'])
            self.__twitter_user = str(cfg['twitter']['search']['user'])

            if not (self.__twitter_keyword and self.__twitter_keyword.strip()) and  not (self.__twitter_user and self.__twitter_user.strip()):
                raise ValueError(
                    'Impostare un valore per almeno uno dei due perametri [user], [keyword]')

            self.__twitter_lang = str(cfg['twitter']['search']['lang'])
            self.__twitter_place_country = str(cfg['twitter']['search']["geo"]['place_country'])
            self.__twitter_place = str(cfg['twitter']['search']["geo"]['place'])
            self.__twitter_bounding_box = str(cfg['twitter']['search']["geo"]['bounding_box'])
            self.__twitter_point_radius = str(cfg['twitter']['search']["geo"]['point_radius']['longitude']) + " " + str(
                cfg['twitter']['search']["geo"]['point_radius']['latitude']) + " " + str(
                cfg['twitter']['search']["geo"]['point_radius']['radius'])

            if self.__twitter_place and self.__twitter_place.strip():
                check.append(True)
            if self.__twitter_place_country and self.__twitter_place_country.strip():
                check.append(True)
            if self.__twitter_bounding_box and self.__twitter_bounding_box.strip():
                check.append(True)
            if self.__twitter_point_radius and self.__twitter_point_radius.strip():
                check.append(True)

            if check.count(True) > 1:
                raise ValueError(
                    'Solo uno tra i paremetri [bounding_box], [point_radius] e [place_country] può essere impostato')

            self.__twitter_context_annotations = cfg['twitter']['search']['context_annotations']
            self.__twitter_n_results = cfg['twitter']['search']['n_results']
            self.__twitter_barer_token = cfg['twitter']['configuration']['barer_token']
            self.__twitter_end_point = cfg['twitter']['configuration']['end_point']

        self.__headers = {"Authorization": "Bearer {}".format(self.__twitter_barer_token)}
        self.__build_query()

    def __next_page(self, next_token=""):
        if next_token != "":
            self.__query["next_token"] = next_token

    def __build_query(self):
        # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
        # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
        self.__query = {'query': ""}
        if self.__twitter_keyword and self.__twitter_keyword.strip():
            self.__query['query'] = self.__twitter_keyword
        if self.__twitter_user and self.__twitter_user.strip():
            if self.__twitter_keyword and self.__twitter_keyword.strip():
                self.__query['query'] += " from: " + self.__twitter_user
            else:
                self.__query['query'] += "from: " + self.__twitter_user
        if self.__twitter_lang and self.__twitter_lang.strip():
            self.__query['query'] += " lang:" + self.__twitter_lang
        if self.__twitter_place and self.__twitter_place.strip():
            self.__query['query'] += " place:" + self.__twitter_place
        if self.__twitter_place_country and self.__twitter_place_country.strip():
            self.__query['query'] += " place_country:" + self.__twitter_place_country
        if self.__twitter_n_results and self.__twitter_n_results.strip():
            self.__query['max_results'] = str(self.__twitter_n_results)
        if self.__twitter_bounding_box and self.__twitter_bounding_box.strip():
            self.__query['query'] += " bounding_box:" + "[" + str(self.__twitter_bounding_box) + "]"
        elif self.__twitter_point_radius and self.__twitter_point_radius.strip() :
            self.__query['query'] += " point_radius:" + "[" + str(self.__twitter_point_radius) + "]"

        self.__query['place.fields'] = "contained_within,country,country_code,full_name,geo,id,name,place_type"
        self.__query['expansions'] = 'geo.place_id,referenced_tweets.id'
        self.__query['tweet.fields'] = 'author_id' + ',public_metrics,entities'
        if self.__twitter_context_annotations:
            self.__query['tweet.fields'] += ',context_annotations'

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
                    if results_to_request < 10:
                        results_to_request = 10
                    if results_to_request > 500:
                        results_to_request = 500
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

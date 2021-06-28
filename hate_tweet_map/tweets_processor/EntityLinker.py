import os

import yaml

from hate_tweet_map.tweets_processor import MyTagMe


class EntityLinker:

    def __init__(self):
        working_directory = os.path.abspath(os.path.dirname(__file__))
        cnfg_file_path = os.path.join(working_directory, "../../script/process_tweets/process_tweets.config")
        with open(cnfg_file_path, "r") as yamlfile:
            cfg = yaml.safe_load(yamlfile)

            self.__tagme_token = cfg['analyzes']['tagme']['token']
            self.__tagme_is_twitter = cfg['analyzes']['tagme']['is_twitter']
            self.__tagme_rho = cfg['analyzes']['tagme']['rho_value']

    def tag(self, raw_tweet, lang):
        MyTagMe.GCUBE_TOKEN = self.__tagme_token

        annotations = MyTagMe.annotate(raw_tweet, lang=lang, is_twitter_text=self.__tagme_is_twitter)

        result = []
        for ann in annotations.get_annotations(float(self.__tagme_rho)):
            result.append(
                ann.mention + " : " + ann.entity_id.__str__() + " : " + ann.entity_title + " : " + ann.uri(lang))
        return result

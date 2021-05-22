import yaml
from yaml import BaseLoader

import MyTagMe


class EntityLinker:

    def __init__(self):
        with open("config.yml", "r") as yamlfile:
            cfg = yaml.load(yamlfile, Loader=BaseLoader)

            self.__tagme_token = cfg['tagme']['token']
            self.__tagme_lang = cfg['tagme']['lang']
            self.__tagme_is_twitter = cfg['tagme']['is_twitter']
            self.__tagme_rho = cfg['tagme']['rho_value']

    def tag(self, raw_tweet):
        MyTagMe.GCUBE_TOKEN = self.__tagme_token

        annotations = MyTagMe.annotate(raw_tweet, lang=self.__tagme_lang, is_twitter_text=self.__tagme_is_twitter)

        # Print annotations with a score higher than 0.2
        result = []
        for ann in annotations.get_annotations(float(self.__tagme_rho)):
            result.append(
                ann.mention + " : " + ann.entity_id.__str__() + " : " + ann.entity_title + " : " + ann.uri(self.__tagme_lang))
        return result

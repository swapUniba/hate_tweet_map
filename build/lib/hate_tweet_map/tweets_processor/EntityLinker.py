'''Entity Linker'''
import os

import yaml

from hate_tweet_map.tweets_processor import MyTagMe


class EntityLinker:
    """

    """
    def __init__(self, path_to_cnfg_file):

        with open(path_to_cnfg_file, "r") as yamlfile:
            cfg = yaml.safe_load(yamlfile)

            self.__tagme_token = cfg['analyzes']['tagme']['token']
            self.__tagme_is_twitter = cfg['analyzes']['tagme']['is_tweet']
            self.__tagme_rho = cfg['analyzes']['tagme']['rho_value']

    def tag(self, raw_tweet: str, lang: str) -> list:

        """
        This method send the text to tag on TagMe service and return the response
        :param raw_tweet: the text of the tweet to tag
        :type raw_tweet: str
        :param lang: tha language to use to tag the entities
        :type lang: str
        :return: a list with the id of the entities, the title and the url of the wikipedia page.
        :rtype: list
        """
        MyTagMe.GCUBE_TOKEN = self.__tagme_token

        annotations = MyTagMe.annotate(raw_tweet, lang=lang, is_twitter_text=self.__tagme_is_twitter)

        result = []
        for ann in annotations.get_annotations(float(self.__tagme_rho)):
            result.append(
                ann.mention + " : " + ann.entity_id.__str__() + " : " + ann.entity_title + " : " + ann.uri(lang))
        return result

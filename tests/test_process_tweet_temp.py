import os
import time
import unittest
from unittest.mock import patch, PropertyMock

from hate_tweet_map.database import DataBase
from hate_tweet_map.tweets_processor.TweetProcessor import ProcessTweet


class TwitterProcessTestCase(unittest.TestCase):
    """ Test cases for Process Class """
    @unittest.skip
    def test_process_sent_it2(self):
        t_to_process = []
        for i in range(0,20000):
            t_to_process.append({
            "_id": i,
            "raw_text": "Olanda: cantante, si presenta in aeroporto con certificato Covid falso, urla per farsi una ragione, ma il Poliziotto lo prende a sberle. E se questo fosse successo in ITALIA sarebbe indagato o dietro le sbarre. Se fosse stato in USA, domani ci sarebbero state le esequie...AMEN... https://t.co/VA8vy9I6XI",
            "author_id": "1236508776544587776",
            "author_name": "Forze Armate e di Polizia",
            "author_username": "FF_AAediPolizia",
            "created_at": "2021-06-25T15:19:38.000Z",
            "lang": "it",
            "possibly_sensitive": False,
            "complete_text": True,
            "twitter_context_annotations": [{
                "domain": {
                    "id": "123",
                    "name": "Ongoing News Story",
                    "description": "Ongoing News Stories like 'Brexit'"
                },
                "entity": {
                    "id": "1220701888179359745",
                    "name": "COVID-19"
                }
            }],
            "referenced_tweets": [{
                "id": "1408441964215873540",
                "type": "retweeted"
            }],
            "twitter_entities": {
                "urls": ["https://t.co/VA8vy9I6XI"],
                "mentions": ["MaccariFranco1"]
            },
            "metrics": {
                "retweet_count": 2,
                "reply_count": 0,
                "like_count": 0,
                "quote_count": 0
            },
            "processed": False,
        })
        with patch.object(DataBase, "extract_new_tweets_to_sentit", return_value=t_to_process):
            with patch.object(DataBase, "update_one") as update_one_mock:
                wk = os.path.dirname(os.path.abspath(__file__))
                f = os.path.join(wk, "process_tweets.config")
                twitter_process = ProcessTweet(f)
                with patch.object(twitter_process, 'feel_it',
                                  new_callable=PropertyMock(return_value=False)):
                    with patch.object(twitter_process, 'nlp',
                                      new_callable=PropertyMock(return_value=False)):
                        with patch.object(twitter_process, 'sent_it',
                                          new_callable=PropertyMock(return_value=True)):
                            with patch.object(twitter_process, 'geo',
                                              new_callable=PropertyMock(return_value=False)):
                                with patch.object(twitter_process, 'tag_me',
                                                  new_callable=PropertyMock(return_value=False)):
                                    with patch.object(twitter_process, 'all_tweets',
                                                      new_callable=PropertyMock(return_value=False)):
                                        s = time.time()
                                        t = twitter_process.sent_it_analyze_sentiment2(t_to_process)
                                        e = time.time()
                                        print(e-s)
                                        self.assertTrue(t)

    def test_process_sent_it3(self):
        t_to_process = []
        for i in range(0,200000):
            t_to_process.append({
            "_id": i,
            "raw_text": "Olanda: cantante, si presenta in aeroporto con certificato Covid falso, urla per farsi una ragione, ma il Poliziotto lo prende a sberle. E se questo fosse successo in ITALIA sarebbe indagato o dietro le sbarre. Se fosse stato in USA, domani ci sarebbero state le esequie...AMEN... https://t.co/VA8vy9I6XI",
            "author_id": "1236508776544587776",
            "author_name": "Forze Armate e di Polizia",
            "author_username": "FF_AAediPolizia",
            "created_at": "2021-06-25T15:19:38.000Z",
            "lang": "it",
            "possibly_sensitive": False,
            "complete_text": True,
            "twitter_context_annotations": [{
                "domain": {
                    "id": "123",
                    "name": "Ongoing News Story",
                    "description": "Ongoing News Stories like 'Brexit'"
                },
                "entity": {
                    "id": "1220701888179359745",
                    "name": "COVID-19"
                }
            }],
            "referenced_tweets": [{
                "id": "1408441964215873540",
                "type": "retweeted"
            }],
            "twitter_entities": {
                "urls": ["https://t.co/VA8vy9I6XI"],
                "mentions": ["MaccariFranco1"]
            },
            "metrics": {
                "retweet_count": 2,
                "reply_count": 0,
                "like_count": 0,
                "quote_count": 0
            },
            "processed": False,
        })
        with patch.object(DataBase, "extract_new_tweets_to_sentit", return_value=t_to_process):
            with patch.object(DataBase, "update_one") as update_one_mock:
                wk = os.path.dirname(os.path.abspath(__file__))
                f = os.path.join(wk, "process_tweets.config")
                twitter_process = ProcessTweet(f)
                with patch.object(twitter_process, 'feel_it',
                                  new_callable=PropertyMock(return_value=False)):
                    with patch.object(twitter_process, 'nlp',
                                      new_callable=PropertyMock(return_value=False)):
                        with patch.object(twitter_process, 'sent_it',
                                          new_callable=PropertyMock(return_value=True)):
                            with patch.object(twitter_process, 'geo',
                                              new_callable=PropertyMock(return_value=False)):
                                with patch.object(twitter_process, 'tag_me',
                                                  new_callable=PropertyMock(return_value=False)):
                                    with patch.object(twitter_process, 'all_tweets',
                                                      new_callable=PropertyMock(return_value=False)):
                                        s = time.time()
                                        t = twitter_process.sent_it_analyze_sentiment2(t_to_process)
                                        e = time.time()
                                        print(e-s)
                                        self.assertTrue(t)

    def test_process_sent_it_understanding_max(self):
        with patch.object(DataBase, "extract_new_tweets_to_sentit", return_value=[]):
            with patch.object(DataBase, "update_one") as update_one_mock:
                wk = os.path.dirname(os.path.abspath(__file__))
                f = os.path.join(wk, "process_tweets.config")
                twitter_process = ProcessTweet(f)
                with patch.object(twitter_process, 'feel_it',
                                  new_callable=PropertyMock(return_value=False)):
                    with patch.object(twitter_process, 'nlp',
                                      new_callable=PropertyMock(return_value=False)):
                        with patch.object(twitter_process, 'sent_it',
                                          new_callable=PropertyMock(return_value=True)):
                            with patch.object(twitter_process, 'geo',
                                              new_callable=PropertyMock(return_value=False)):
                                with patch.object(twitter_process, 'tag_me',
                                                  new_callable=PropertyMock(return_value=False)):
                                    with patch.object(twitter_process, 'all_tweets',
                                                      new_callable=PropertyMock(return_value=False)):
                                        n = 300000
                                        t_to_process = self.build(n)
                                        print('asking for:{}'.format(n))
                                        s = time.time()
                                        t = twitter_process.sent_it_analyze_sentiment2(t_to_process)
                                        e = time.time()
                                        if t:
                                            print('succeeded at:{}'.format(n))
                                            print('time:{}'.format(e - s))
                                            while t:
                                                n = n+100000
                                                print('asking fot:{}'.format(n))
                                                t_to_process = self.build(n)
                                                s = time.time()
                                                t = twitter_process.sent_it_analyze_sentiment2(t_to_process)
                                                e = time.time()
                                                print('succeeded at:{}'.format(n))
                                                print('time:{}'.format(e - s))
                                            print('failed at:{}'.format(n))

    def build(self, n):
        t_to_process = []
        for i in range(0, n):
            t_to_process.append({
                "_id": i,
                "raw_text": "Olanda: cantante, si presenta in aeroporto con certificato Covid falso, urla per farsi una ragione, ma il Poliziotto lo prende a sberle. E se questo fosse successo in ITALIA sarebbe indagato o dietro le sbarre. Se fosse stato in USA, domani ci sarebbero state le esequie...AMEN... https://t.co/VA8vy9I6XI",
                "author_id": "1236508776544587776",
                "author_name": "Forze Armate e di Polizia",
                "author_username": "FF_AAediPolizia",
                "created_at": "2021-06-25T15:19:38.000Z",
                "lang": "it",
                "possibly_sensitive": False,
                "complete_text": True,
                "twitter_context_annotations": [{
                    "domain": {
                        "id": "123",
                        "name": "Ongoing News Story",
                        "description": "Ongoing News Stories like 'Brexit'"
                    },
                    "entity": {
                        "id": "1220701888179359745",
                        "name": "COVID-19"
                    }
                }],
                "referenced_tweets": [{
                    "id": "1408441964215873540",
                    "type": "retweeted"
                }],
                "twitter_entities": {
                    "urls": ["https://t.co/VA8vy9I6XI"],
                    "mentions": ["MaccariFranco1"]
                },
                "metrics": {
                    "retweet_count": 2,
                    "reply_count": 0,
                    "like_count": 0,
                    "quote_count": 0
                },
                "processed": False,
            })
        return t_to_process


if __name__ == "__main__":
    unittest.main()  # run all tests

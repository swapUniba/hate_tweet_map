import logging
import time
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch, PropertyMock

from hate_tweet_map.database import DataBase
from script.process_tweets.process_tweets import Process


class TwitterProcessTestCase(unittest.TestCase):
    """ Test cases for Process Class """

    def test_process_entity_linker(self):
        t_to_process = [{
            "_id": "1408444783182352394",
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
        }]
        with patch.object(DataBase, "extract_new_tweets_to_tag", return_value=t_to_process):
            with patch.object(DataBase, "update_one") as update_one_mock:
                twitter_process = Process()
                with patch.object(twitter_process, 'feel_it',
                                  new_callable=PropertyMock(return_value=False)):
                    with patch.object(twitter_process, 'nlp',
                                      new_callable=PropertyMock(return_value=False)):
                        with patch.object(twitter_process, 'sent_it',
                                          new_callable=PropertyMock(return_value=False)):
                            with patch.object(twitter_process, 'geo',
                                              new_callable=PropertyMock(return_value=False)):
                                with patch.object(twitter_process, 'tag_me',
                                                  new_callable=PropertyMock(return_value=True)):
                                    with patch.object(twitter_process, 'all_tweets',
                                                      new_callable=PropertyMock(return_value=False)):
                                        t_processed = {
                                            "_id": "1408444783182352394",
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
                                            "tags": {
                                                "tag_me": [
                                                    "Olanda : 77670 : Repubblica delle Sette Province Unite : https://it.wikipedia.org/wiki/Repubblica_delle_Sette_Province_Unite",
                                                    "aeroporto : 286 : Aeroporto : https://it.wikipedia.org/wiki/Aeroporto",
                                                    "ITALIA : 2340360 : Italia : https://it.wikipedia.org/wiki/Italia",
                                                    "USA : 1563740 : Stati Uniti d'America : https://it.wikipedia.org/wiki/Stati_Uniti_d'America",
                                                    "AMEN : 1715399 : Amen. : https://it.wikipedia.org/wiki/Amen."]
                                            }
                                        }
                                        twitter_process.start()
                                        update_one_mock.assert_called_with(t_processed)

    def test_process_nlp(self):
        t_to_process = [{
            "_id": "1408444783182352394",
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
        }]
        with patch.object(DataBase, "extract_new_tweets_to_nlp", return_value=t_to_process):
            with patch.object(DataBase, "update_one") as update_one_mock:
                twitter_process = Process()
                with patch.object(twitter_process, 'feel_it',
                                  new_callable=PropertyMock(return_value=False)):
                    with patch.object(twitter_process, 'nlp',
                                      new_callable=PropertyMock(return_value=True)):
                        with patch.object(twitter_process, 'sent_it',
                                          new_callable=PropertyMock(return_value=False)):
                            with patch.object(twitter_process, 'geo',
                                              new_callable=PropertyMock(return_value=False)):
                                with patch.object(twitter_process, 'tag_me',
                                                  new_callable=PropertyMock(return_value=False)):
                                    with patch.object(twitter_process, 'all_tweets',
                                                      new_callable=PropertyMock(return_value=False)):
                                        t_processed = {

                                            "_id": "1408444783182352394",
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
                                            "processed": True,
                                            "spacy": {
                                                "processed_text": ["Olanda POS : PROPN MORPH : ",
                                                                   "cantare POS : NOUN MORPH : Number=Sing",
                                                                   "presentire POS : VERB MORPH : Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
                                                                   "aeroporto POS : NOUN MORPH : Gender=Masc|Number=Sing",
                                                                   "certificare POS : NOUN MORPH : Gender=Masc|Number=Sing",
                                                                   "Covid POS : PROPN MORPH : ",
                                                                   "falsare POS : ADJ MORPH : Gender=Masc|Number=Sing",
                                                                   "urlo POS : NOUN MORPH : Gender=Fem|Number=Plur",
                                                                   "farsi POS : VERB MORPH : Clitic=Yes|Person=3|PronType=Prs|VerbForm=Inf",
                                                                   "ragione POS : NOUN MORPH : Gender=Fem|Number=Sing",
                                                                   "Poliziotto POS : PROPN MORPH : ",
                                                                   "prendere POS : VERB MORPH : Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin",
                                                                   "sberle POS : VERB MORPH : Clitic=Yes|Gender=Fem|Number=Plur|Person=3|PronType=Prs|VerbForm=Inf",
                                                                   "E POS : CCONJ MORPH : ",
                                                                   "fossa POS : AUX MORPH : Mood=Sub|Number=Sing|Person=3|Tense=Imp|VerbForm=Fin",
                                                                   "succedere POS : VERB MORPH : Gender=Masc|Number=Sing|Tense=Past|VerbForm=Part",
                                                                   "ITALIA POS : PROPN MORPH : ",
                                                                   "indagare POS : VERB MORPH : Gender=Masc|Number=Sing|Tense=Past|VerbForm=Part",
                                                                   "o POS : CCONJ MORPH : ",
                                                                   "sbarra POS : NOUN MORPH : Gender=Fem|Number=Plur",
                                                                   "fossa POS : AUX MORPH : Mood=Sub|Number=Sing|Person=3|Tense=Imp|VerbForm=Fin",
                                                                   "stare POS : VERB MORPH : Gender=Masc|Number=Sing|Tense=Past|VerbForm=Part",
                                                                   "USA POS : PROPN MORPH : ",
                                                                   "domani POS : ADV MORPH : ",
                                                                   "stare POS : VERB MORPH : Gender=Fem|Number=Plur|Tense=Past|VerbForm=Part",
                                                                   "esequia POS : NOUN MORPH : Gender=Fem|Number=Plur",
                                                                   "AMEN POS : PROPN MORPH : ",
                                                                   "https://t.co/VA8vy9I6XI POS : NOUN MORPH : "],
                                                "entities": ["Olanda : LOC", "Covid falso : MISC",
                                                             "Poliziotto : PER", "ITALIA : ORG", "USA : LOC"]
                                            }
                                        }
                                        twitter_process.start()
                                        update_one_mock.assert_called_with(t_processed)

    def test_process_sent_it(self):
        t_to_process = [{
            "_id": "1408444783182352394",
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
        }]
        with patch.object(DataBase, "extract_new_tweets_to_sentit", return_value=t_to_process):
            with patch.object(DataBase, "update_one") as update_one_mock:
                twitter_process = Process()
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
                                        t_processed = {
                                            "_id": "1408444783182352394",
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
                                            "sentiment": {
                                                "sent-it": {
                                                    "subjectivity": "subj",
                                                    "sentiment": "negative"
                                                }
                                            }
                                        }
                                        twitter_process.start()
                                        update_one_mock.assert_called_with(t_processed)

    def test_process_feel_it(self):
        t_to_process = [{
            "_id": "1408444783182352394",
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
        }]
        with patch.object(DataBase, "extract_new_tweets_to_feel_it", return_value=t_to_process):
            with patch.object(DataBase, "update_one") as update_one_mock:
                twitter_process = Process()
                with patch.object(twitter_process, 'feel_it',
                                  new_callable=PropertyMock(return_value=True)):
                    with patch.object(twitter_process, 'nlp',
                                      new_callable=PropertyMock(return_value=False)):
                        with patch.object(twitter_process, 'sent_it',
                                          new_callable=PropertyMock(return_value=False)):
                            with patch.object(twitter_process, 'geo',
                                              new_callable=PropertyMock(return_value=False)):
                                with patch.object(twitter_process, 'tag_me',
                                                  new_callable=PropertyMock(return_value=False)):
                                    with patch.object(twitter_process, 'all_tweets',
                                                      new_callable=PropertyMock(return_value=False)):
                                        t_processed = {
                                            "_id": "1408444783182352394",
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
                                            "sentiment": {
                                                "feel-it": {
                                                    "emotion": "anger",
                                                    "sentiment": "negative"
                                                }
                                            }
                                        }
                                        twitter_process.start()
                                        update_one_mock.assert_called_with(t_processed)

    def test_process_geo_user_location(self):
        t_to_process = [{
            "_id": "1408442636743106563",
            "raw_text": "Olanda: cantante, si presenta in aeroporto con certificato Covid falso, urla per farsi una ragione, ma il Poliziotto lo prende a sberle. E se questo fosse successo in ITALIA sarebbe indagato o dietro le sbarre. Se fosse stato in USA, domani ci sarebbero state le esequie...AMEN... https://t.co/VA8vy9I6XI",
            "author_id": "100964035",
            "author_name": "Umberto Liuzzo",
            "author_username": "umbertoliuzzo",
            "created_at": "2021-06-25T15:11:06.000Z",
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
            "geo": {
                "user_location": "Bronte -CT - Sicilia",
            },
            "metrics": {
                "retweet_count": 2,
                "reply_count": 0,
                "like_count": 0,
                "quote_count": 0
            },
            "processed": False,
        }]
        with patch.object(DataBase, "extract_new_tweets_to_geo", return_value=t_to_process):
            with patch.object(DataBase, "update_one") as update_one_mock:
                twitter_process = Process()
                with patch.object(twitter_process, 'feel_it',
                                  new_callable=PropertyMock(return_value=False)):
                    with patch.object(twitter_process, 'nlp',
                                      new_callable=PropertyMock(return_value=False)):
                        with patch.object(twitter_process, 'sent_it',
                                          new_callable=PropertyMock(return_value=False)):
                            with patch.object(twitter_process, 'geo',
                                              new_callable=PropertyMock(return_value=True)):
                                with patch.object(twitter_process, 'tag_me',
                                                  new_callable=PropertyMock(return_value=False)):
                                    with patch.object(twitter_process, 'all_tweets',
                                                      new_callable=PropertyMock(return_value=False)):
                                        t_processed = {
                                            "_id": "1408442636743106563",
                                            "raw_text": "Olanda: cantante, si presenta in aeroporto con certificato Covid falso, urla per farsi una ragione, ma il Poliziotto lo prende a sberle. E se questo fosse successo in ITALIA sarebbe indagato o dietro le sbarre. Se fosse stato in USA, domani ci sarebbero state le esequie...AMEN... https://t.co/VA8vy9I6XI",
                                            "author_id": "100964035",
                                            "author_name": "Umberto Liuzzo",
                                            "author_username": "umbertoliuzzo",
                                            "created_at": "2021-06-25T15:11:06.000Z",
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
                                            "geo": {
                                                "user_location": "Bronte -CT - Sicilia",
                                                "coordinates": {
                                                    "latitude": 37.7871598,
                                                    "longitude": 14.8338448
                                                }
                                            },
                                            "metrics": {
                                                "retweet_count": 2,
                                                "reply_count": 0,
                                                "like_count": 0,
                                                "quote_count": 0
                                            },
                                            "processed": False,
                                        }
                                        twitter_process.start()
                                        update_one_mock.assert_called_with(t_processed)

    def test_process_geo_city_country(self):
        t_to_process = [{
            "_id": "1408441964215873540",
            "raw_text": "Olanda: cantante, si presenta in aeroporto con certificato Covid falso, urla per farsi una ragione, ma il Poliziotto lo prende a sberle. E se questo fosse successo in ITALIA sarebbe indagato o dietro le sbarre. Se fosse stato in USA, domani ci sarebbero state le esequie...AMEN... https://t.co/VA8vy9I6XI",
            "author_id": "959362502453878785",
            "author_name": "Maccari Franco",
            "author_username": "MaccariFranco1",
            "created_at": "2021-06-25T15:08:26.000Z",
            "lang": "it",
            "possibly_sensitive": False,
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
            "twitter_entities": {
                "urls": ["https://t.co/VA8vy9I6XI"]
            },
            "geo": {
                "geo_id": "662bb543f9dc0cf6",
                "country": "Italia",
                "city": "Catanzaro, Calabria",
            },
            "metrics": {
                "retweet_count": 2,
                "reply_count": 0,
                "like_count": 4,
                "quote_count": 0
            },
            "processed": False
        }]
        with patch.object(DataBase, "extract_new_tweets_to_geo", return_value=t_to_process):
            with patch.object(DataBase, "update_one") as update_one_mock:
                twitter_process = Process()
                with patch.object(twitter_process, 'feel_it',
                                  new_callable=PropertyMock(return_value=False)):
                    with patch.object(twitter_process, 'nlp',
                                      new_callable=PropertyMock(return_value=False)):
                        with patch.object(twitter_process, 'sent_it',
                                          new_callable=PropertyMock(return_value=False)):
                            with patch.object(twitter_process, 'geo',
                                              new_callable=PropertyMock(return_value=True)):
                                with patch.object(twitter_process, 'tag_me',
                                                  new_callable=PropertyMock(return_value=False)):
                                    with patch.object(twitter_process, 'all_tweets',
                                                      new_callable=PropertyMock(return_value=False)):
                                        t_processed = {
                                            "_id": "1408441964215873540",
                                            "raw_text": "Olanda: cantante, si presenta in aeroporto con certificato Covid falso, urla per farsi una ragione, ma il Poliziotto lo prende a sberle. E se questo fosse successo in ITALIA sarebbe indagato o dietro le sbarre. Se fosse stato in USA, domani ci sarebbero state le esequie...AMEN... https://t.co/VA8vy9I6XI",
                                            "author_id": "959362502453878785",
                                            "author_name": "Maccari Franco",
                                            "author_username": "MaccariFranco1",
                                            "created_at": "2021-06-25T15:08:26.000Z",
                                            "lang": "it",
                                            "possibly_sensitive": False,
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
                                            "twitter_entities": {
                                                "urls": ["https://t.co/VA8vy9I6XI"]
                                            },
                                            "geo": {
                                                "geo_id": "662bb543f9dc0cf6",
                                                "country": "Italia",
                                                "city": "Catanzaro, Calabria",
                                                "coordinates": {
                                                    "latitude": 38.82996034999999,
                                                    "longitude": 16.43155687627833
                                                }
                                            },
                                            "metrics": {
                                                "retweet_count": 2,
                                                "reply_count": 0,
                                                "like_count": 4,
                                                "quote_count": 0
                                            },
                                            "processed": False,
                                        }
                                        twitter_process.start()
                                        update_one_mock.assert_called_with(t_processed)


if __name__ == "__main__":
    unittest.main()  # run all tests

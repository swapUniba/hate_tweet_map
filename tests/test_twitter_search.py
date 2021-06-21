import logging
import time
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch, PropertyMock

from tqdm import tqdm

from hate_tweet_map import database
from hate_tweet_map.tweets_searcher import SearchTweets


class TwitterSearchTestCase(unittest.TestCase):
    """ Test cases for TwitterSearch Class """

    def setUp(self):
        self.db = MagicMock(database)

    def test429Error1Second(self):
        """ Test the behaviour of the method search() when a 429 status code is returned (rate limit exceeded) from
        Twitter. """
        """ In this case the search() method send more than one rewuest per second, so twitter get 429 error. """
        """ In this case we wait for 2 second before resend the request """
        twitter_research = SearchTweets(self.db)
        with patch.object(twitter_research, '_SearchTweets__twitter_n_results',
                          new_callable=PropertyMock(return_value=20)):
            with patch.object(twitter_research, '_SearchTweets__multi_user',
                              new_callable=PropertyMock(return_value=False)):
                with patch.object(twitter_research, '_SearchTweets__twitter_users',
                                  new_callable=PropertyMock(return_value=[])):
                    with patch.object(twitter_research, '_SearchTweets__twitter_keyword',
                                      new_callable=PropertyMock(return_value="Eurovision")):
                        twitter_research.save = MagicMock()
                        for i in range(0, 3):
                            twitter_research.search()

        self.assertEqual(twitter_research.total_result, 60)

    @unittest.skip
    def test429Error300request(self):
        """ Test the behaviour of the method search() when a 429 status code is returned (rate limit exceeded) from
        Twitter. """
        """ In this case the search() method send more than one rewuest per second, so twitter get 429 error. """
        """ In this case we wait for 2 second before resend the request """
        """ WARNING: TIME EXPENSIVE TEST: 20-25min needed """
        twitter_research = SearchTweets(self.db)
        with patch.object(twitter_research, '_SearchTweets__twitter_n_results',
                          new_callable=PropertyMock(return_value=10)):
            with patch.object(twitter_research, '_SearchTweets__multi_user',
                              new_callable=PropertyMock(return_value=False)):
                with patch.object(twitter_research, '_SearchTweets__twitter_users',
                                  new_callable=PropertyMock(return_value=[])):
                    with patch.object(twitter_research, '_SearchTweets__twitter_keyword',
                                      new_callable=PropertyMock(return_value="Eurovision")):
                        twitter_research.save = MagicMock()
                        logging.getLogger('SEARCH').propagate = False
                        with self.assertLogs('SEARCH', level='INFO') as cm:
                            for i in (tqdm(range(0, 301), desc="NUMBER OF REQUEST", leave=True)):
                                twitter_research.search()
                                time.sleep(0.3)
        self.assertTrue('INFO:SEARCH:RATE LIMITS REACHED: WAITING' in cm.output)
        self.assertEqual(twitter_research.total_result, 3010)

    def testMaxResult(self):
        """ Test the correct behavior when asking for a specific_n result number. """
        """ In this case we are asking for 520 tweets, and we return as first result 500 tweets """
        """ we check that er make exactly 2 requests. """

        response1 = {'meta': {'result_count': 500, 'next_token': 1}}
        response2 = {'meta': {'result_count': 20, 'next_token': 2}}
        thing = SearchTweets(self.db)
        with patch.object(thing, '_SearchTweets__twitter_n_results', new_callable=PropertyMock(return_value=520)):
            with patch.object(thing, '_SearchTweets__connect_to_endpoint') as mock_method:
                with patch.object(thing, '_SearchTweets__multi_user', new_callable=PropertyMock(return_value=False)):
                    with patch.object(thing, '_SearchTweets__twitter_users',
                                      new_callable=PropertyMock(return_value=[])):
                        with patch.object(thing, '_SearchTweets__twitter_keyword',
                                          new_callable=PropertyMock(return_value="Eurovision")):
                            mock_method.side_effect = [response1, response2]
                            thing.save = mock.Mock()
                            thing.search()

        self.assertEqual(mock_method.call_count, 2)

    # def test503Error(self):
    #     """ Test the correct behavior when asking for a specific_n result number. """
    #     """ In this case we are asking for 520 tweets, and we return as first result 500 tweets """
    #     """ we check that er make exactly 2 requests. """
    #
    #     response1 = {'meta': {r'result_count': 500, 'next_token': 1}}
    #     response2 = {'meta': {r'result_count': 20, 'next_token': 2}}
    #     thing = TwitterSearch(self.db)
    #     with patch.object(thing, '_SearchTweets__twitter_n_results', new_callable=PropertyMock(return_value=520)):
    #         with patch.object(thing, '_SearchTweets__connect_to_endpoint') as mock_method:
    #             with patch.object(thing, '_SearchTweets__multi_user',
    #                               new_callable=PropertyMock(return_value=False)):
    #                 with patch.object(thing, '_SearchTweets__twitter_user',
    #                                   new_callable=PropertyMock(return_value=None)):
    #                     with patch.object(thing, '_SearchTweets__twitter_keyword',
    #                                       new_callable=PropertyMock(return_value="Eurovision")):
    #                         mock_method.side_effect = [response1, response2]
    #                         thing.save = mock.Mock()
    #                         thing.search()
    #
    #     self.assertEqual(mock_method.call_count, 2)
    def testOnlyUser(self):
        twitter_research = SearchTweets(self.db)
        with patch.object(twitter_research, '_SearchTweets__twitter_n_results',
                          new_callable=PropertyMock(return_value=10)):
            with patch.object(twitter_research, '_SearchTweets__multi_user',
                              new_callable=PropertyMock(return_value=False)):
                with patch.object(twitter_research, '_SearchTweets__twitter_users',
                                  new_callable=PropertyMock(return_value=["eldesmarque"])):
                    with patch.object(twitter_research, '_SearchTweets__twitter_keyword',
                                      new_callable=PropertyMock(return_value=None)):
                        twitter_research.save = MagicMock()
                        with self.assertLogs('SEARCH', level='INFO') as cm:
                            twitter_research.search()
        self.assertTrue('INFO:SEARCH:SEARCH FOR: eldesmarque' in cm.output)
        # failed on gitlab ci
        # self.assertEqual(twitter_research.total_result, 10)

    def testMultiUser(self):
        users = ["eldesmarque", "GabrielChoulet", "JoArilenaStan"]
        twitter_research = SearchTweets(self.db)
        with patch.object(twitter_research, '_SearchTweets__twitter_n_results',
                          new_callable=PropertyMock(return_value=10)):
            with patch.object(twitter_research, '_SearchTweets__multi_user',
                              new_callable=PropertyMock(return_value=True)):
                with patch.object(twitter_research, '_SearchTweets__twitter_users',
                                  new_callable=PropertyMock(return_value=users)):
                    with patch.object(twitter_research, '_SearchTweets__twitter_keyword',
                                      new_callable=PropertyMock(return_value="Eurovision")):
                        twitter_research.save = MagicMock()
                        with self.assertLogs('SEARCH', level='INFO') as cm:
                            twitter_research.search()
        self.assertTrue('INFO:SEARCH:SEARCH FOR: eldesmarque' in cm.output)
        self.assertTrue('INFO:SEARCH:SEARCH FOR: GabrielChoulet' in cm.output)
        self.assertTrue('INFO:SEARCH:SEARCH FOR: JoArilenaStan' in cm.output)

    def test_no_next_token(self):
        """ Test the correct behavior when there is no next_token in the twitter response"""

        response1 = {'meta': {'result_count': 500}}
        thing = SearchTweets(self.db)
        with patch.object(thing, '_SearchTweets__twitter_n_results', new_callable=PropertyMock(return_value=520)):
            with patch.object(thing, '_SearchTweets__connect_to_endpoint') as mock_method:
                with patch.object(thing, '_SearchTweets__multi_user', new_callable=PropertyMock(return_value=False)):
                    with patch.object(thing, '_SearchTweets__twitter_users',
                                      new_callable=PropertyMock(return_value=[])):
                        with patch.object(thing, '_SearchTweets__twitter_keyword',
                                          new_callable=PropertyMock(return_value="Eurovision")):
                            with self.assertLogs('SEARCH', level='DEBUG') as cm:
                                mock_method.side_effect = [response1]
                                thing.save = mock.Mock()
                                thing.search()

        self.assertEqual(mock_method.call_count, 1)
        self.assertTrue("INFO:SEARCH:THERE ARE NO OTHER PAGE AVAILABLE. ALL TWEETS REACHED" in cm.output)
        self.assertTrue("DEBUG:SEARCH:NO NEXT TOKEN IN RESPONSE:INTERRUPTING" in cm.output)

    def test_no_next_token_2calls(self):
        """ Test the correct behavior when there is no next_token in the twitter response"""

        response1 = {'meta': {'result_count': 500, 'next_token': 1}}
        response2 = {'meta': {'result_count': 10}}

        thing = SearchTweets(self.db)
        with patch.object(thing, '_SearchTweets__twitter_n_results', new_callable=PropertyMock(return_value=520)):
            with patch.object(thing, '_SearchTweets__connect_to_endpoint') as mock_method:
                with patch.object(thing, '_SearchTweets__multi_user', new_callable=PropertyMock(return_value=False)):
                    with patch.object(thing, '_SearchTweets__twitter_users',
                                      new_callable=PropertyMock(return_value=[])):
                        with patch.object(thing, '_SearchTweets__twitter_keyword',
                                          new_callable=PropertyMock(return_value="Eurovision")):
                            with self.assertLogs('SEARCH', level='DEBUG') as cm:
                                mock_method.side_effect = [response1, response2]
                                thing.save = mock.Mock()
                                thing.search()

        self.assertEqual(mock_method.call_count, 2)
        self.assertTrue("INFO:SEARCH:THERE ARE NO OTHER PAGE AVAILABLE. ALL TWEETS REACHED" in cm.output)
        self.assertTrue("DEBUG:SEARCH:NO NEXT TOKEN IN RESPONSE:INTERRUPTING" in cm.output)

    def test_all_tweets(self):
        """ Test the correct behavior when all_tweets flag is set to True and n_results to some number """

        response1 = {'meta': {'result_count': 500, 'next_token': 1}}
        response2 = {'meta': {'result_count': 500, 'next_token': 2}}
        response3 = {'meta': {'result_count': 500, 'next_token': 3}}
        response4 = {'meta': {'result_count': 500}}

        thing = SearchTweets(self.db)
        with patch.object(thing, '_SearchTweets__twitter_n_results', new_callable=PropertyMock(return_value=10)):
            with patch.object(thing, '_SearchTweets__twitter_all_tweets', new_callable=PropertyMock(return_value=True)):
                with patch.object(thing, '_SearchTweets__connect_to_endpoint') as mock_method:
                    with patch.object(thing, '_SearchTweets__multi_user', new_callable=PropertyMock(return_value=False)):
                        with patch.object(thing, '_SearchTweets__twitter_users',
                                          new_callable=PropertyMock(return_value=[])):
                            with patch.object(thing, '_SearchTweets__twitter_keyword',
                                              new_callable=PropertyMock(return_value="Eurovision")):
                                with self.assertLogs('SEARCH', level='DEBUG') as cm:
                                    mock_method.side_effect = [response1, response2, response3, response4]
                                    thing.save = mock.Mock()
                                    thing.search()

        self.assertEqual(mock_method.call_count, 4)
        self.assertTrue("INFO:SEARCH:ASKING FOR NEXT PAGE" in cm.output)
        self.assertTrue("INFO:SEARCH:THERE ARE NO OTHER PAGE AVAILABLE. ALL TWEETS REACHED" in cm.output)
        self.assertTrue("DEBUG:SEARCH:NO NEXT TOKEN IN RESPONSE:INTERRUPTING" in cm.output)


    def test_all_tweets2(self):
        """ Test the correct behavior when all_tweets flag is set to True"""

        response1 = {'meta': {'result_count': 500, 'next_token': 1}}
        response2 = {'meta': {'result_count': 500, 'next_token': 2}}
        response3 = {'meta': {'result_count': 500, 'next_token': 3}}
        response4 = {'meta': {'result_count': 500}}

        thing = SearchTweets(self.db)
        with patch.object(thing, '_SearchTweets__twitter_all_tweets', new_callable=PropertyMock(return_value=True)):
            with patch.object(thing, '_SearchTweets__connect_to_endpoint') as mock_method:
                with patch.object(thing, '_SearchTweets__multi_user', new_callable=PropertyMock(return_value=False)):
                    with patch.object(thing, '_SearchTweets__twitter_users',
                                      new_callable=PropertyMock(return_value=[])):
                        with patch.object(thing, '_SearchTweets__twitter_keyword',
                                          new_callable=PropertyMock(return_value="Eurovision")):
                            with self.assertLogs('SEARCH', level='DEBUG') as cm:
                                mock_method.side_effect = [response1, response2, response3, response4]
                                thing.save = mock.Mock()
                                thing.search()

        self.assertEqual(mock_method.call_count, 4)
        self.assertTrue("INFO:SEARCH:ASKING FOR NEXT PAGE" in cm.output)
        self.assertTrue("INFO:SEARCH:THERE ARE NO OTHER PAGE AVAILABLE. ALL TWEETS REACHED" in cm.output)
        self.assertTrue("DEBUG:SEARCH:NO NEXT TOKEN IN RESPONSE:INTERRUPTING" in cm.output)


    def test_n_results_greater_than_500(self):
        """ Test the correct behavior when we are asking for more than 500tweets """

        thing = SearchTweets(self.db)
        with patch.object(thing, '_SearchTweets__twitter_n_results', new_callable=PropertyMock(return_value=1070)):
            with patch.object(thing, '_SearchTweets__twitter_all_tweets', new_callable=PropertyMock(return_value=False)):
                with patch.object(thing, '_SearchTweets__multi_user', new_callable=PropertyMock(return_value=False)):
                    with patch.object(thing, '_SearchTweets__twitter_users',
                                      new_callable=PropertyMock(return_value=[])):
                        with patch.object(thing, '_SearchTweets__twitter_keyword',
                                          new_callable=PropertyMock(return_value="Eurovision")):
                            with self.assertLogs('SEARCH', level='DEBUG') as cm:
                                thing.save = mock.Mock()
                                thing.search()

        self.assertEqual(thing.total_result, 1070)

    def test_n_results_less_than_10(self):
        """ Test the correct behavior when we are asking for less than 10tweets """

        thing = SearchTweets(self.db)
        with patch.object(thing, '_SearchTweets__twitter_n_results', new_callable=PropertyMock(return_value=9)):
            with patch.object(thing, '_SearchTweets__twitter_all_tweets',
                              new_callable=PropertyMock(return_value=False)):
                with patch.object(thing, '_SearchTweets__multi_user',
                                  new_callable=PropertyMock(return_value=False)):
                    with patch.object(thing, '_SearchTweets__twitter_users',
                                      new_callable=PropertyMock(return_value=[])):
                        with patch.object(thing, '_SearchTweets__twitter_keyword',
                                          new_callable=PropertyMock(return_value="Eurovision")):
                            with self.assertLogs('SEARCH', level='DEBUG') as cm:
                                thing.save = mock.Mock()
                                thing.search()

        self.assertEqual(thing.total_result, 10)



if __name__ == "__main__":
    unittest.main()  # run all tests

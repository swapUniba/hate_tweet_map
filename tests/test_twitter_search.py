import logging
import time
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch, PropertyMock

from tqdm import tqdm

import util
from DataBase import DataBase
from TwitterSearch import TwitterSearch


class TwitterSearchTestCase(unittest.TestCase):
    """ Test cases for TwitterSearch Class """

    def setUp(self):
        self.db = MagicMock(DataBase)

    def test429Error1Second(self):
        """ Test the behaviour of the method search() when a 429 status code is returned (rate limit exceeded) from
        Twitter. """
        """ In this case the search() method send more than one rewuest per second, so twitter get 429 error. """
        """ In this case we wait for 2 second before resend the request """
        twitter_research = TwitterSearch(self.db)
        with patch.object(twitter_research, '_TwitterSearch__twitter_n_results',
                          new_callable=PropertyMock(return_value=20)):
            with patch.object(twitter_research, '_TwitterSearch__multi_user',
                              new_callable=PropertyMock(return_value=False)):
                with patch.object(twitter_research, '_TwitterSearch__twitter_user',
                                  new_callable=PropertyMock(return_value=None)):
                    with patch.object(twitter_research, '_TwitterSearch__twitter_keyword',
                                      new_callable=PropertyMock(return_value="Eurovision")):
                        twitter_research.save = MagicMock()
                        for i in range(0, 3):
                            twitter_research.search()

        self.assertEqual(twitter_research.total_result, 60)

    def test429Error300request(self):
        """ Test the behaviour of the method search() when a 429 status code is returned (rate limit exceeded) from
        Twitter. """
        """ In this case the search() method send more than one rewuest per second, so twitter get 429 error. """
        """ In this case we wait for 2 second before resend the request """
        """ WARNING: TIME EXPENSIVE TEST: 20-25min needed """
        twitter_research = TwitterSearch(self.db)
        with patch.object(twitter_research, '_TwitterSearch__twitter_n_results',
                          new_callable=PropertyMock(return_value=10)):
            with patch.object(twitter_research, '_TwitterSearch__multi_user',
                              new_callable=PropertyMock(return_value=False)):
                with patch.object(twitter_research, '_TwitterSearch__twitter_user',
                                  new_callable=PropertyMock(return_value=None)):
                    with patch.object(twitter_research, '_TwitterSearch__twitter_keyword',
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

        response1 = {'meta': {r'result_count': 500, 'next_token': 1}}
        response2 = {'meta': {r'result_count': 20, 'next_token': 2}}
        thing = TwitterSearch(self.db)
        with patch.object(thing, '_TwitterSearch__twitter_n_results', new_callable=PropertyMock(return_value=520)):
            with patch.object(thing, '_TwitterSearch__connect_to_endpoint') as mock_method:
                with patch.object(thing, '_TwitterSearch__multi_user', new_callable=PropertyMock(return_value=False)):
                    with patch.object(thing, '_TwitterSearch__twitter_user',
                                      new_callable=PropertyMock(return_value=None)):
                        with patch.object(thing, '_TwitterSearch__twitter_keyword',
                                          new_callable=PropertyMock(return_value="Eurovision")):
                            mock_method.side_effect = [response1, response2]
                            thing.save = mock.Mock()
                            thing.search()

        self.assertEqual(mock_method.call_count, 2)


if __name__ == "__main__":
    unittest.main()  # run all tests

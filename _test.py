import unittest
from unittest import mock
from unittest.mock import MagicMock, patch, PropertyMock
from DataBase import DataBase
from TwitterSearch import TwitterSearch


class TwitterSearchTestCase(unittest.TestCase):
    """ Test cases for TwitterSearch Class """

    def setUp(self):
        self.db = MagicMock(DataBase)
        self.twitter_research = TwitterSearch(self.db)

        # self.twitter_research.search()

    def test429Error(self):
        """ Test the behaviour of the method search() when a 429 status code is returned (rate limit exceeded) from Twitter. """
        """ In this case the search() method wait for the reset of the rate limit and then resend the request."""
        """ WARNING: TIME EXPENSIVE TEST: 15min needed """
        for i in range(0, 3):
            self.twitter_research.search()
        assert self.twitter_research.total_result == 30

    def testMaxResult(self):
        """ Test the correct behavior when asking for a specific_n result number. """
        """ In this case we are asking for 520 tweets, and we return as first result 500 tweets """
        """ we check that er make exactly 2 requests. """

        response1 = {'meta': {r'result_count': 500, 'next_token': 1}}
        response2 = {'meta': {r'result_count': 20, 'next_token': 2}}
        thing = TwitterSearch(self.db)
        with patch.object(thing, '_TwitterSearch__twitter_n_results', new_callable=PropertyMock(return_value=520)):
            with patch.object(thing, '_TwitterSearch__connect_to_endpoint') as mock_method:
                mock_method.side_effect = [response1, response2]
                thing.save = mock.Mock()
                thing.search()

        self.assertEqual(mock_method.call_count, 2)


if __name__ == "__main__":
    unittest.main()  # run all tests

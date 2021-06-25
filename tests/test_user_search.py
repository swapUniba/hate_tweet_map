import unittest
from unittest.mock import patch


from hate_tweet_map.database import DataBase
from script.search_users.search_user import UserSearch


class UsersSearchTestCase(unittest.TestCase):
    """ Test cases for UserSearch Class """

    @patch.object(DataBase, 'get_users')
    @patch.object(DataBase, 'get_users_id')
    def test_no_valid_id(self, mock_get_users_id, mock_get_users):
        with self.assertLogs('SEARCH USERS', level='WARNING') as cm:
            mock_get_users_id.return_value = ['2']
            mock_get_users.return_value = []
            usr = UserSearch()
            with patch.object(usr, '_UserSearch__save') as mock_method:
                usr.search()
        self.assertTrue("WARNING:SEARCH USERS:IMPOSSIBLE TO RETRIEVE THE FOLLOWING USERS:['2']" in cm.output)

    @patch.object(DataBase, 'get_users')
    @patch.object(DataBase, 'get_users_id')
    def test_not_only_valid_id(self, mock_get_users_id, mock_get_users):
        with self.assertLogs('SEARCH USERS', level='WARNING') as cm:
            mock_get_users_id.return_value = ['2', "857925504514523137"]
            mock_get_users.return_value = []
            usr = UserSearch()
            with patch.object(usr, '_UserSearch__save') as mock_method:
                usr.search()
        self.assertTrue("WARNING:SEARCH USERS:IMPOSSIBLE TO RETRIEVE THE FOLLOWING USERS:['2']" in cm.output)
        self.assertTrue("INFO:SEARCH USERS:USERS RECEIVED: 1" in cm.output)

    @patch.object(DataBase, 'get_users')
    @patch.object(DataBase, 'get_users_id')
    def test_more_than_100_users(self, mock_get_users_id, mock_get_users):
        with self.assertLogs('SEARCH USERS', level='WARNING') as cm:
            r = []
            for i in range(0, 101):
                r.append("857925504514523137")
            mock_get_users_id.return_value = r
            mock_get_users.return_value = []
            usr = UserSearch()
        with patch.object(usr, '_UserSearch__save') as mock_method:
            usr.search()
        self.assertTrue(mock_method.call_count, 2)

    @patch.object(DataBase, 'get_users')
    @patch.object(DataBase, 'get_users_id')
    def test_more_than_100_users2(self, mock_get_users_id, mock_get_users):
        with self.assertLogs('SEARCH USERS', level='INFO') as cm:
            r = []
            for i in range(0, 1000):
                r.append("857925504514523137")
            mock_get_users_id.return_value = r
            mock_get_users.return_value = []
            usr = UserSearch()
            with patch.object(usr, '_UserSearch__save') as mock_method:
                usr.search()
        self.assertTrue(mock_method.call_count, 10)

    @patch.object(DataBase, 'get_users')
    @patch.object(DataBase, 'get_users_id')
    def test_more_than_100_users3(self, mock_get_users_id, mock_get_users):
        r = []
        for i in range(0, 1000):
            r.append("857925504514523137")
        mock_get_users_id.return_value = r
        mock_get_users.return_value = []
        usr = UserSearch()
        with patch.object(usr, '_UserSearch__save') as mock_method:
            usr.search()
        self.assertTrue(mock_method.call_count, 10)

    @patch.object(DataBase, 'get_users')
    @patch.object(DataBase, 'get_users_id')
    @unittest.skip
    def test_429_error(self, mock_get_users_id, mock_get_users):
        with self.assertLogs('SEARCH USERS', level='INFO') as cm:
            r = []
            for i in range(0, 1000 * 100):
                r.append("857925504514523137")
            mock_get_users_id.return_value = r
            mock_get_users.return_value = []
            usr = UserSearch()
            with patch.object(usr, '_UserSearch__save') as mock_method:
                usr.search()
        self.assertTrue(mock_method.call_count, 10)
        self.assertTrue("INFO:SEARCH USERS:USERS RECEIVED: 100" in cm.output)


if __name__ == "__main__":
    unittest.main()  # run all tests

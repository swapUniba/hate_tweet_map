from hate_tweet_map.users_searcher.SearchUsers import UserSearch


def main():
    usr = UserSearch('search_users.config')
    usr.search()


if __name__ == "__main__":
    main()

.. Hate Tweet Map documentation master file, created by
   sphinx-quickstart on Tue Jun 29 17:23:39 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Search Tweets Script
====================

.. toctree::
   :maxdepth: 5
   :caption: Contents:

Configuration file
------------------
To search tweets on twitter the first thing to do is edit
the configuration file search_tweets.config in the script/search_tweets folder.
The configuration file looks like this:

.. code:: yaml

   mongodb:
       # default url
       url: mongodb://localhost:27017/
       database:
       collection:
   twitter:
       configuration:
           barer_token: AAAAAAAAAAAAAAAAAAAAAAPtPgEAAAAAoVlZ4I0szkcu4dL%2Bhqif%2F%2BF45Oo%3DJbvSo773bskLu1GexDv9Dq1HjuSjfSwfxgLdDXEdlPO5mKyE6G
           end_point: https://api.twitter.com/2/tweets/search/all
       search:
           # MANDATORY:
           # Please fill at least one of the following fields. If both fields are set it's possible to search for a twitter with the given keyword tweeted by the specific user.

           # enter the keyword/s to search for on twitter. It's also possible use logical operators. If no logical operator are specified all keywords will be searched in AND.
           # the AND operator is handle by a space, so to search "Joe AND Trump" just write "Joe Trump", the OR operator is "OR".
           # for example: "Joe Biden", "Biden OR Trump", "(Biden OR Trump) whitehouse" (the last query means: "(Biden OR Trump) AND whitehouse").
           keyword:

           # enter the username or the user id to search for tweets of a specific user.
           user:

           #OPTIONAL:
           # the language of the tweets
           lang:

           # enable/disable the twitter context annotation in the twitter response
           context_annotations: True

           # the max results of tweets
           n_results: 10
           # possible value: True/False
           # if this field is set to True the value on n_result it automatically overwrite and set to 500.
           all_tweets: False
           # please see here for information about time fields: https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all
           # you can set:
               # 1. only start_time: if you specify only start time but no end time, end time will be assumed to be current time (-30 sec). (see https://twittercommunity.com/t/twitter-api-v2-search-endpoint-what-is-start-time-and-end-time-actual-default/152679)
               # 2. only end_time: If you specify only end time, start time will be assumed 30 days before the end time specified. (see https://twittercommunity.com/t/twitter-api-v2-search-endpoint-what-is-start-time-and-end-time-actual-default/152679)
               # 3. both: the tweets in the range specified
               # 4. none: By default, a request will return Tweets from up to 30 days ago if you do not include this parameters. (see https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all)
           time:
               # format: YYYY-MM-DDTHH:mm:ssZ (ISO 8601/RFC 3339)
               # example value: 2018-10-19T07:20:50.52+00:00
               start_time:
               end_time:
           # geo parameter.
           # only one of the following fields could be set
           geo:
               place:
               place_country:
               # example value: -105.301758 39.964069 -105.178505 40.09455
               bounding_box:
               # please if you want search by point radius set all the parameters in the point_radius section.
               point_radius:
                   # example value: 2.355128
                   longitude:
                   # 48.861118
                   latitude:
                   # 16km
                   radius:
           #Possible values: True/False. When is True only tweet that are not retweet are retrieved. default value: False.
           filter_retweet: False


Mandatory Section
^^^^^^^^^^^^^^^^^
The mandatory section is this one:

.. code:: yaml

   search:
           # MANDATORY:
           # Please fill at least one of the following fields. If both fields are set it's possible to search for a twitter with the given keyword tweeted by the specific user.

           # enter the keyword/s to search for on twitter. It's also possible use logical operators. If no logical operator are specified all keywords will be searched in AND.
           # the AND operator is handle by a space, so to search "Joe AND Trump" just write "Joe Trump", the OR operator is "OR".
           # for example: "Joe Biden", "Biden OR Trump", "(Biden OR Trump) whitehouse" (the last query means: "(Biden OR Trump) AND whitehouse").
           keyword:

           # enter the username or the user id to search for tweets of a specific user.
           user:

As explained in the comments in the keywords section it is possible
set the keyword (s) that tweets must contain. To search using the logical operator
just use the parentheses and the keyword OR and the space for AND.

In the user field you can enter the user's ID or username.
Note that at least one of these two fields must be set.
It is also possible to set both fields, which means "search
tweets containing this [keyword] from this [user]".

Optional Section
^^^^^^^^^^^^^^^^

The optional section is:

.. code:: yaml

   #OPTIONAL:
        # the language of the tweets
        lang:

        # enable/disable the twitter context annotation in the twitter response
        context_annotations: True

        # the max results of tweets
        n_results: 10
        # possible value: True/False
        # if this field is set to True the value on n_result it automatically overwrite and set to 500.
        all_tweets: False
        # please see here for information about time fields: https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all
        # you can set:
            # 1. only start_time: if you specify only start time but no end time, end time will be assumed to be current time (-30 sec). (see https://twittercommunity.com/t/twitter-api-v2-search-endpoint-what-is-start-time-and-end-time-actual-default/152679)
            # 2. only end_time: If you specify only end time, start time will be assumed 30 days before the end time specified. (see https://twittercommunity.com/t/twitter-api-v2-search-endpoint-what-is-start-time-and-end-time-actual-default/152679)
            # 3. both: the tweets in the range specified
            # 4. none: By default, a request will return Tweets from up to 30 days ago if you do not include this parameters. (see https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all)
        time:
            # format: YYYY-MM-DDTHH:mm:ssZ (ISO 8601/RFC 3339)
            # example value: 2018-10-19T07:20:50.52+00:00
            start_time:
            end_time:
        # geo parameter.
        # only one of the following fields could be set
        geo:
            place:
            place_country:
            # example value: -105.301758 39.964069 -105.178505 40.09455
            bounding_box:
            # please if you want search by point radius set all the parameters in the point_radius section.
            point_radius:
                # example value: 2.355128
                longitude:
                # 48.861118
                latitude:
                # 16km
                radius:
        #Possible values: True/False. When is True only tweet that are not retweet are retrieved. default value: False.
        filter_retweet: False


As shown is composed by 7 sub-section:

    | `1. Lang`_
    | `2. Context Annotation`_
    | `3. Number of results`_
    | `4. Reach all tweets`_
    | `5. Time`_
    | `6. Geo`_
    | `7. Filter retweet`_

1. Lang
"""""""
.. code:: yaml

        # the language of the tweets
        lang:

This field indicate the language of the tweets that you
want retrieve.

| From Twitter Api Doc:

*Restricts tweets to the given language, given by an* `ISO 639-1 code`_ .
*Language detection is best-effort.*

.. _ISO 639-1 code: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes

| An example values: it, en, pt, es.

| **Possible values**: *any ISO-639-1 code*

2. Context Annotation
"""""""""""""""""""""
.. code:: yaml

   # enable/disable the twitter context annotation in the twitter response
   context_annotations: True


| This field indicate to Twitter to include or not the context annotation for tweet that have it.
| For more information see the official doc `here. <https://developer.twitter.com/en/docs/twitter-api/annotations>`_

**Possible values**: *True/False*

3. Number of results
""""""""""""""""""""
.. code:: yaml

   # the max results of tweets
   n_results: 10


| This field indicate to Twitter to how may tweets the response should contain.
| Twiiter allow to search for minimum 10 tweets to maximum 500 tweets for request.
| So if the value insert in this field is less than 10 this field automatically will be set to 10; if the value insert is greater than 500 more requests will be send to Twitter.
| Note that Twitter to reach a number of tweets as close as possible to the value given here.

| **Possible values**: *any int number*.

| N.B
| If the :code:`all_tweets` field is set to True this field automatically will be set to 500 whatever value is insert here.


4. Reach all tweets
"""""""""""""""""""
.. code:: yaml

   # if this field is set to True the value on n_result it automatically overwrite and set to 500.
   all_tweets: False

| When a research is send to Twitter it responds with the number of tweets asked and, if possible, with a :code:`next_token`, this token allow to go to the next page of results.
| So this field indicate to the script to iterate all over the pages returned by Twitter.
| In this case the :code:`n_results` field will be set automatically to 500 to obtain 500 tweets per time.

| **Possible values**: *True/False*.

| N.B
| Setting this field to True means start a very time expensive research.

5. Time
"""""""
.. code:: yaml

   # please see here for information about time fields: https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all
   # you can set:
      # 1. only start_time: if you specify only start time but no end time, end time will be assumed to be current time (-30 sec). (see https://twittercommunity.com/t/twitter-api-v2-search-endpoint-what-is-start-time-and-end-time-actual-default/152679)
      # 2. only end_time: If you specify only end time, start time will be assumed 30 days before the end time specified. (see https://twittercommunity.com/t/twitter-api-v2-search-endpoint-what-is-start-time-and-end-time-actual-default/152679)
      # 3. both: the tweets in the range specified
      # 4. none: By default, a request will return Tweets from up to 30 days ago if you do not include this parameters. (see https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all)
   time:
      # format: YYYY-MM-DDTHH:mm:ssZ (ISO 8601/RFC 3339)
      # example value: 2018-10-19T07:20:50.52+00:00
      start_time:
      end_time:


| This field allow to search tweets in a specific range of time.
| There 4 possible configuration:

      #. only :code:`start_time`: if you specify only start time but no :code:`end_time`, :code:`end_time` will be assumed to be current time (-30 sec).
      #. only :code:`end_time`: if you specify only :code:`end_time`, :code:`start_time` will be assumed 30 days before the :code:`end_time` specified.
      #. both: the tweets in the range specified
      #. none: by default, a request will return tweets from up to 30 days ago if you do not include this parameters.

| For more information see:

   * `<https://twittercommunity.com/t/twitter-api-v2-search-endpoint-what-is-start-time-and-end-time-actual-default/152679>`_
   * `<https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all>`_

| The values in this fields must be in the ISO 8601/RFC 3339 format, so: *YYYY-MM-DDTHH:mm:ss+Z*.
| An example value is: *2018-10-19T07:20:50.52+00:00* where *00:00* is the time zone.

| **Possible values**: *any date in ISO 8601/RFC 3339 format.*

6. Geo
""""""
.. code:: yaml

   geo:
         place:
         place_country:
         # example value: -105.301758 39.964069 -105.178505 40.09455
         bounding_box:
         # please if you want search by point radius set all the parameters in the point_radius section.
         point_radius:
             # example value: 2.355128
             longitude:
             # 48.861118
             latitude:
             # 16km
             radius:


| In this section it is possible to set the geographical parameters, in this way it is possible to filter the tweets based on their geographical origin.
| The possible parameters are, please note that **Only one of these fields must be set**:

   | - *place*:
   | matches tweets tagged with the specified location or twitter place ID. Multi-word place names (“New York City”, “Palo Alto”) should be enclosed in quotes.

   | **Possible values**: *any name of city, enclosed in quotes if the place names ia s multi/word.*

   | - *place_country*:
   | attaches tweets where the country code associated with a tagged place/location matches the given ISO alpha-2 character code.
   | You can find a list of valid ISO codes `here <https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2>`_

   | **Possible values**: *any name of country in ISO_3166-1_alpha-2 format.*

   | - *bounding_box*:
   | matches against the place.geo.coordinates object of the Tweet when present, and in Twitter, against a place geo polygon, where the place polygon is fully contained within the defined region.
   | :code:`bounding_box: west_long south_lat east_long north_lat`

      * :code:`west_long south_lat` represent the southwest corner of the bounding box where :code:`west_long` is the longitude of that point, and :code:`south_lat` is the latitude.
      * :code:`east_long north_lat` represent the northeast corner of the bounding box, where :code:`east_long` is the longitude of that point, and :code:`north_lat` is the latitude.
      * Width and height of the bounding box must be less than 25mi
      * Longitude is in the range of ±180
      * Latitude is in the range of ±90
      * All coordinates are in decimal degrees.

   | **Possible values**: *4 coordinates in decimal degrees.*
   | **Example**: :code:`bounding_box: -105.301758 39.964069 -105.178505 40.09455`

   | - *point_radius*:
   | matches against the place.geo.coordinates object of the Tweet when present, and in Twitter, against a place geo polygon, where the Place polygon is fully contained within the defined region.

      * longitude:
         | longitude is in the range of ±180
         | **Possible values**: *a coordinate in decimal degrees.*
         | **Example**: :code:`longitude: 48.861118`

      * latitude:
         | latitude is in the range of ±90
         | **Possible values**: *a coordinate in decimal degrees.*
         | **Example**: :code:`longitude: 48.861118`

      * radius:
         | radius must be less than 25mi; units of radius supported are miles (mi) and kilometers (km); radius must be less than 25mi
         | **Possible values**: *an integer number followed by the string 'km' or 'mi' to indicate if the value refer to kilometers or miles.*
         | **Example**: :code:`radius: 10km`


   See here for more information:

   * `<https://developer.twitter.com/en/docs/tutorials/filtering-tweets-by-location>`_
   * `<https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query>`_

7. Filter retweet
"""""""""""""""""
.. code:: yaml

   #Possible values: True/False. When is True only tweet that are not retweet are retrieved. default value: False.
   filter_retweet: False

| This field indicate to Twitter to include or not the retweet in the response.
| If is True Twitter response could contain also retweet, if false not.

**Possible values**: *True/False*

Use the script
--------------

After editing and setting the configuration file just open a terminal in the folder script/search_tweets and launch this command:

.. code::

   python search_tweets.py


.. Hate Tweet Map documentation master file, created by
   sphinx-quickstart on Tue Jun 29 17:23:39 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Search Users Script
====================

.. toctree::
   :maxdepth: 5
   :caption: Contents:

This script allow to search information about a list of users. Specfically this tools read the tweets from a collection, save the users id  and then
search the information about these users.

Configuration file
------------------
To search users on twitter the first thing to do is edit
the configuration file search_users.config in the script/search_users folder.
The configuration file looks like this:

.. code:: yaml

   mongodb_tweets:
       url: mongodb://localhost:27017/
       database:
       collection:
   mongodb_users:
       url: mongodb://localhost:27017/
       database:
       collection:

   twitter:
       configuration:
           barer_token: AAAAAAAAAAAAAAAAAAAAAAPtPgEAAAAAoVlZ4I0szkcu4dL%2Bhqif%2F%2BF45Oo%3DJbvSo773bskLu1GexDv9Dq1HjuSjfSwfxgLdDXEdlPO5mKyE6G
           end_point: https://api.twitter.com/2/users



Mongodb tweets
^^^^^^^^^^^^^^

.. code:: yaml

   mongodb_tweets:
       url: mongodb://localhost:27017/
       database:
       collection:

This section contains information necessary to connect to the mongo db collection where the tweets are saved and retrieve from it the users ID.

Mongodb Users
^^^^^^^^^^^^^

.. code:: yaml

   mongodb_users:
       url: mongodb://localhost:27017/
       database:
       collection:

This section contains information necessary to connect to the mongo db collection where save the users information obtained from Twitter.

Twitter
^^^^^^^

.. code:: yaml

   twitter:
       configuration:
           barer_token: AAAAAAAAAAAAAAAAAAAAAAPtPgEAAAAAoVlZ4I0szkcu4dL%2Bhqif%2F%2BF45Oo%3DJbvSo773bskLu1GexDv9Dq1HjuSjfSwfxgLdDXEdlPO5mKyE6G
           end_point: https://api.twitter.com/2/users

This section contains information necessary to connect to Twitter API.
Don't change the value of :code:`end_point` field if you really don't know what are you doing.
The :code:`barer_token` field it's related to an Twitter App with research privileges.

Use the script
--------------

After editing and setting the configuration file just open a terminal in the folder script/search_users and launch this command:

.. code::

   python search_users.py

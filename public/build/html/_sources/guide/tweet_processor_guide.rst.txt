.. Hate Tweet Map documentation master file, created by
   sphinx-quickstart on Tue Jun 29 17:23:39 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Process Tweets Script
=====================

.. toctree::
   :maxdepth: 5
   :caption: Contents:

This script allow to perform 5 different types of analysis on thw saved tweets.
The possible analysis are:

   * *Entity Linker*: uses the TagMe service to find entities in the text of the tweet and to connect these with the respective wikipedia page.
   * *Geo*: if present uses the geographic information in the tweet to find the coordinates of the place where the tweet have benn posted. Uses Open Street Map service. (This operation could be time expensive cause OSM allows to send only one request per second.)
   * *Natural Language Processing*: uses spacy model to lemmatize the text of the tweet. In addition save the POS and the Morphological information and the entities found by spacy in the text.
   * *Sentiment Analysis*: uses two different services, sent-it and feel-it, to perform the sentiment analysis of the tweet. Note that feel/it algorithm works only with italian tweets.

Note that there are two mode to select the tweets to analyze:

   * all the tweets in the collection
   * only the tweets that have not yet been passed to the Natural Language Phase.

To choose the first mode just set the :code:`analyze_all_tweets` to :code:`True` otherwise to :code:`False`.

To better understand this mechanism see this:

.. code::

   If analyze_all_tweets is False
   ------------------ If geocode=True
   ----------------------------------look for tweet not geocoded yet
   ----------------------------------geocode the tweet (regardless NLP tasks)
   ------------------ If NLP=True
   --------------------------------- look for tweet not processed
   --------------------------------- process the tweet
   etc.

   If analyze_all_tweets is True
   ------------------ If geocode=True
   ---------------------------------- geocode all the tweets (and overwrite previous information)
   ------------------ If NLP=True
   ---------------------------------- process again all the tweets (and overwrite previous information)
   etc.

   accordingly,
   if I set: analyze_all_tweets=True, geocode=True, nlp=False, I only run geocode on all the tweets, regardless the state of the NLP processing.





Configuration file
------------------
To process tweets the first thing to do is to edit the configuration file process_tweets.config in the script/tweets_processor folder.
The configuration file looks like this:

.. code:: yaml

   mongodb:
       url: mongodb://localhost:27017/
       database:
       collection:
   analyses:
       nlp: True
       tagme:
           enabled: True
           token: 7f5391f2-142e-4fd5-9cc9-56e91c4c9add-843339462
           lang: it
           is_twitter: True
           rho_value: 0.15
       sentiment_analyze:
           sent_it: True
           feel_it: True
       geocoding: True
       analyze_all_tweets: False

Mongodb
^^^^^^^

.. code::

   mongodb:
       url: mongodb://localhost:27017/
       database:
       collection:

This section provide the information to connect to the mongodb collection where the tweets to process are saved.

Analyses:Nlp
^^^^^^^^^^^^

.. code:: yaml

   analyzes:
      nlp: True

| This section enables or disables the SpaCy's Natural Language Processing.
| **Possible values:** True/False

Analyses:TagMe
^^^^^^^^^^^^^^

.. code:: yaml

    analyses:
       tagme:
           enabled: True
           token: 7f5391f2-142e-4fd5-9cc9-56e91c4c9add-843339462
           is_tweet: True
           rho_value: 0.15

This section enables Entity Linker phase using TagMe service.

   * :code:`enabled:`:
      | enable or disable this phase.
      | **Possible values:** True/False

   * :code:`token:`:
      | the token obtained from TagMe to send the requests. See `here <https://sobigdata.d4science.org/web/tagme/tagme-help>`_ for more info.
      | **Possible values:** a valid TagMe token

   * :code:`is_tweet:`:
      | indicate to TagMe service if the text given is a tweet or not.
      | **Possible values:** True/False

   * :code:`rho_value:`:
      | estimates the confidence in the annotation. (Note that ρ does not indicate the relevance of the entity in the input text). You can use the ρ value to discard annotations that are below a given threshold. The threshold should be chosen in the interval [0,1]. A reasonable threshold is between 0.1 and 0.3.
      | **Possible values:** any number between 0 and 1

Analyses:Sentiment Analyses
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: yaml

    analyses:
       sentiment_analyze:
              sent_it: True
              feel_it: True

This section enables Sentiment Analyses phase.

   * :code:`sent-it:`:
      | enable or disable sent-it phase.
      | **Possible values:** True/False

   * :code:`feel-it:`:
      | enable or disable sent-it phase.
      | Note that this phase will disable automatically in presence of english tweet.
      | **Possible values:** True/False

Analyses:Geocoding
^^^^^^^^^^^^^^^^^^

.. code:: yaml

       geocoding: True

| This section enables or disables the geocoding phase using Open Street Map service.
| **Possible values:** True/False


Analyses:Analyze all tweets
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: yaml

       analyze_all_tweets: False

| This section indicate to analyze all tweets in the mongodb collection or not.
| **Possible values:** True/False


Use the script
--------------

After editing and setting the configuration file just open a terminal in the folder script/process_tweets and launch this command:

.. code::

   python process_tweets.py
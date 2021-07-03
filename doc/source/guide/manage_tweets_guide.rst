.. Hate Tweet Map documentation master file, created by
   sphinx-quickstart on Tue Jun 29 17:23:39 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Manage Tweets Script
=====================

.. toctree::
   :maxdepth: 5
   :caption: Contents:


Using this script is possible:
    - extract some tweets from the database and save it on .json or .csv file
    - delete some tweets

The criteria to select the tweets to extract/delete are defined in the manage_tweets.config file.
Is possible modify that file to set the criteria.
The possible criteria are:
   - contains some specific word/words. In this case it is possible or write a list of words separated by comma in the words field, or use a txt file and write it path in the path field.
   - contains a specific sentiment
   - contains a word with a specific Part Of Speech (POS)
   - raw criteria: a query written in mongodb style

These criteria and the words specified in the relative field/file are connected with the "OR" logical operator
or with the "AND" logical operator. It is possible specify which operator must be used setting the logical_operator field in the config file.



Configuration file
------------------
To process tweets the first thing to do is to edit the configuration file process_tweets.config in the script/manage_tweets folder.
The configuration file looks like this:

.. code:: yaml

    mongodb:
        url: mongodb://localhost:27017/
        database:
        collection:
    #possible values: extract delete
    mode:
    #json or csv (only with extract mode)
    format:
    criteria:
      #possible values: negative positive neutral
      sentiment:
      #a list of keywords separated by a comma
      keywords:
        words:
        path:
      postag:
      #a raw NoSql query
      raw_query:
      #possible value: and or. This field specify with which logical operator the fields must be connected
      logical_operator: or

Mongodb
^^^^^^^

.. code::

   mongodb:
       url: mongodb://localhost:27017/
       database:
       collection:

This section provide the information to connect to the mongodb collection where the tweets to manage are saved.
**Mandatory**

Mode
^^^^^

.. code:: yaml

   #possible values: extract delete
      mode: extract

| The mode indicates what the script have to do. As explain before it's possible extract and save in a file the tweets or delete it.
| **Possible values:** extract delete
| **Mandatory**

extract:format
""""""""""""""

.. code:: yaml

  #possible values: extract delete
    mode: extract
    #json or csv (only with extract mode)
    format:

| To extract tweets it's necessary set the :code:`mode: extract` and to choose a format so: or :code:`format: csv` or :code:`format: json`.


delete
""""""

.. code:: yaml

  #possible values: extract delete
    mode: delete
    #json or csv (only with extract mode)
    format:

| To delete tweets it's necessary set the :code:`mode: delete` and leaves blank the :code:`format` field.



Criteria
^^^^^^^^

.. code:: yaml

    criteria:
      #possible values: negative positive neutral
      sentiment:
      #a list of keywords separated by a comma
      keywords:
        words:
        path:
      postag:
      #a raw NoSql query
      raw_query:
      #possible value: and or. This field specify with which logical operator the fields must be connected
      logical_operator: or

This section set the criteria to find the tweets in the db (to delete or extract it)

   * :code:`sentiment:`:
      | setting this field it's possible retrieve tweets with a specific sentiment, in particular choosing between tweets with neutral or positive or negative sentiment.
      | **Possible values:** negative/positive/neutral
      | **Optional**


   * :code:`keywords:`:
      | setting this field it's possible retrieve tweets that contains specific words
      | N.B if the :code:`logical_operator` it's set to :code:`or` will be retrieved tweets that have one of the words spcified here,
      | otherwise if the field it's set to :code:`and` will be retrieved only tweets that contains all the specified words.
      * :code:`words:`:
         | a list of words to search separeted by a comma
         | **Possible values:** a list of words separated by a comma
         | **Example value:** sun,sea,island
         | **Optional**
      * :code:`path:`:
         | the path to a .txt file contained the words to search.
         | The .txt file have to contain each word to search in a different line, example:

         .. code::

               sun
               sea
               island

         | **Possible values:** a valid path to a .txt file
         | **Optional**

   * :code:`postag:`:
      | setting this field it's possible retrieve tweets that contains a word with a specific POS tag.
      | For more info see:

         * `here for a generic understanding <https://spacy.io/usage/linguistic-features>`_
         * `here for a complete list of italian SpaCy's POS values (see labels scheme section in it_core_news_lg) <https://spacy.io/models/it#it_core_news_lg-labels>`_
         * `here for a complete list of english SpaCy's POS values (see labels scheme section in en_core_web_lg) <https://spacy.io/models/en#en_core_web_lg-labels>`_

      | **Possible values:** any valid POS value
      | **Example value:** ADV
      | **Optional**

   * :code:`raw_query:`:
      | setting this field it's possible to write a own query.
      | the query must be a mongodb query and have to take in account the fields of the tweet saved in the collection.
      | **Possible values:** any valid mongodb query
      | **Example value:** {'processed':True}
      | **Optional**

   * :code:`logical_operator:`:
      | if more than one criteria field are set or if the keywprds field it' set it's necessary to define how logically connect this criteria or the words specified, so if using :code:`and` logical operator or :code:`or` logical operator.
      | **Possible values:** or/and
      | **Mandatory**

Use the script
--------------

After editing and setting the configuration file just open a terminal in the folder script/manage_tweets and launch this command:

.. code::

   python manage_tweets.py



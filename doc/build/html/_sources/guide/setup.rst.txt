.. Hate Tweet Map documentation master file, created by
   sphinx-quickstart on Tue Jun 29 17:23:39 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Initialization
====================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Setup
-----
To use the Hate Tweet Map tools it's sufficient install it and  the requires module,
so just open a terminal, clone the repository: move into the root directory of the project and run the se

.. code::

   git clone https://github.com/swapUniba/hate_tweet_map.git hate_tweet_map

Then run:

.. code::

   cd hate_tweet_map
   pip install -r requirements.txt
   pip install setuptools
   python setup.py install
   python setup.py install_lib

Nota that the project requires python3, so make sure that your python version is 3 or higher, if you have more than one python version installed maybe
in the above commands you have to substitute "python" with "python3" and "pip" with "pip3".

If after this you have some problems try to run the above commands with root privileges (sudo for linux system and cmd as administrator for win system)

That's all.


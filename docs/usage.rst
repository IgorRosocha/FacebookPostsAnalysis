Usage
======

Now that you are all set up, you're ready to use **FacebookPostsAnalysis**! Application uses command line interface for its functionality:

.. code:: python

    analysis [COMMAND] [OPTIONS] [ARGUMENTS]

If you wish to list all of the available options and commands in your command line interface, just type 

.. code:: python

	analysis

or

.. code:: python

	analysis --help

To get the posts of a **Facebook** open group/page, you have to use the command **get_posts** this way:

.. click:: FacebookPostsAnalysis.analysis:get_posts
   :prog: get_posts
   :show-nested:

.. note::  You can choose from two **ENTITY** arguments: **page** or **group** (depends on which you want to analyze).

The command will automatically gather all of the posts data, generate a .csv file containing all of it in a structured, demonstrative way and create a **Jupyter Notebook** containing the full analysis.

These two files will be located in the analysis folder, named **analysis_{id}.csv/ipynb**.

Please proceed to `Working with the Jupyter Notebook <jupyter.html#section>`__.
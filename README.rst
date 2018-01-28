=====================
FacebookPostsAnalysis
=====================

**FacebookPostsAnalysis** (`MI-PYT@FIT CTU`_ semestral work) is a Python 3.6 application to analyze the posts of a Facebook page or open group - total number of reactions, most liked posts, activity of users, and much more. All of the posts are exported into a .csv file, which can be opened with your preferred spreadsheet software, and then automatically analyzed using **Jupyter Notebook**.

To see the example .csv file / notebook, please see the examples folder.

--------------------------------------------------------------------------------

Installation
-------------

There are two ways how to install **FacebookPostsAnalysis**:

1. Installation directly from TestPyPI, using the following command: 

``python -m pip install --extra-index-url https://test.pypi.org/pypi FacebookPostsAnalysis``

2. If any problem occurred, please follow these steps:
	
- Download **FacebookPostsAnalysis** directly from TestPyPI `here <https://testpypi.python.org/pypi/FacebookPostsAnalysis>`_.
- Unpack the download .tar.gz file.
- Use the following command in the labelord directory: ``python setup.py install``


Please note that **FacebookPostsAnalysis** requires at least Python 3.6 to be installed to run properly!

Usage
-----
In order to successfully cooperate with **Facebook Graph API**, every user has to register and configure his own App, which is bounded with **APP ID** and **APP SECRET**. For **FacebookPostsAnalysis** to work properly, you need to specify these in the **configuration file** (see config.cfg), along with the ID of Facebook open page/group you want to analyze.

After proper specification of your credentials and Facebook open page/group ID in configuration file, you are ready to use **FacebookPostsAnalysis**. Application uses command line interface for its functionality:

.. code:: python

    analysis get_posts [OPTIONS] [ENTITY]
    
You can use the following options to specify the desired time period/range:

``--until``: Date until when to analyse Facebook posts.

``--since``: Date since when to analyse Facebook posts.

``--year``: Year to analyse Facebook posts.

The ENTITY argument is also required. You can choose from two ENTITY arguments:
``page`` or ``group`` (depends on which you want to analyze).

For more information about the usage of **FacebookPostsAnalysis**, please see the documentation.

Documentation
--------------

For the full documentation, please visit `Readthedocs.io <http://labelord-igorrosocha.readthedocs.io/en/latest/>`__.

You can also build the documentation locally. Just follow these steps:

1. Download **FacebookPostsAnalysis** and install it (in the main directory: ``python setup.py install``)
2. Navigate to **docs** directory
3. Run ``python -m pip install -r requirements.txt``
4. Run ``pip install sphinx-click``
5. Run ``make html`` and ``make doctest``
6. You can find all of the .html files in _build/html directory

License
-------

This project is licensed under the **MIT License**.


.. _MI-PYT@FIT CTU: https://github.com/cvut/MI-PYT

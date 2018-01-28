Configuration
=================

To initialize the configuration of **FacebookPostsAnalysis** properly, you first need to initialize your personal **APP ID** and **APP SECRET**, in order to successfully communicate with **Facebook Graph API**.

APP ID and APP SECRET
----------------------

In order to successfully cooperate with **Facebook Graph API**, every user has to register and configure his own App, which is bounded with **APP ID** and **APP SECRET**. For **FacebookPostsAnalysis** to work properly, these are required. You can generate your own following these steps:

	- login to **Facebook**,
	- upgrade your personal **Facebook** account to a **Facebook Developer** account (skip this step, if you already have a developer account),
	- choose **Apps** in the header navigation and select **Add a New App**,
	- choose a name for your app (for example analysis) and select **Create New Facebook App ID**,
	- now you can find your **APP ID** and **APP SECRET** in your app's dashboard.

Now you are able to copy your newly created **APP ID** and **APP SECRET** and specify them. These need to be specified in your `Configuration file`_.


Configuration file
-------------------

The configuration file, which is used to specify the open group/page to analyze, has to be located in the analysis directory (by default) with the name provided ``./config.cfg``.

You can also specify your own path to the configuration file, using the ``-c/--config`` option when running from CLI.

Configuration file has to contain these fields:

	- ``[credentials]``
		- ``app_id``: your Facebook APP ID,
		- ``app_secret``: your Facebook APP SECRET.
		
		.. warning:: **Don't forget to keep your APP ID and APP SECRET safe and never publish them!**

	- ``[facebook]``
		- ``group_id``: the ID of a Facebook open group you want to analyze,
		- ``page_id``: the ID of a Facebook page you want to analyze.

Example configuration file
---------------------------

::

   [credentials]
   app_id = ENTER_YOUR_FACEBOOK_APP_ID_HERE
   app_secret = ENTER_YOUR_FACEBOOK_APP_SECRET_HERE

   [facebook]
   group_id = ENTER_GROUP_ID_HERE
   page_id = ENTER_PAGE_ID_HERE

Please proceed to `Usage <usage.html#section>`__.
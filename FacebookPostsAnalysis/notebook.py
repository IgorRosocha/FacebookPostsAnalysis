import nbformat as nbf


def create_notebook(entity_id):
    """
    Create a Jupyter Notebook, containing the full analysis of Facebook group/page.

    :param entity_id: ID of Facebook group/page
    """
    nb = nbf.v4.new_notebook()
    header = '# Facebook Posts Analysis\n' \
             'Analysis based on data gathered from Facebook page/group.\n\n' \
             'For more information, please check the documentation or ' \
             'visit https://github.com/IgorRosocha/FacebookPostsAnalysis\n\n' \
             'ID of analyzed group/page: {}'.format(entity_id)

    images = '<img src="https://github.com/IgorRosocha/FacebookPostsAnalysis/blob/master/' \
             'FacebookPostsAnalysis/static/images/Python.png?raw=true" style="width: 100px; float: left;"/>\n\n' \
             '<img src="https://github.com/IgorRosocha/FacebookPostsAnalysis/blob/master/' \
             'FacebookPostsAnalysis/static/images/Facebook.png?raw=true" style="width: 100px; float: left;"/>\n\n' \
             '<img src="https://github.com/IgorRosocha/FacebookPostsAnalysis/blob/master/' \
             'FacebookPostsAnalysis/static/images/Pandas.png?raw=true" style="width: 400px; float: left;"/>'

    imports = 'import pandas as pd\n' \
              'import matplotlib\n' \
              'import numpy as np\n' \
              'import calendar\n\n' \
              '%matplotlib inline'

    number_header = '### 1. Total number of posts:'
    number_of_posts = 'results = pd.read_csv("analysis_csv_{}.csv", index_col=None)\n'.format(entity_id) + \
                      'number_of_posts = results["ID"].count()\n' \
                      'print("Total number of posts: {}".format(number_of_posts))'

    popular_header = '### 2. Most popular posts:'
    popular_posts = 'def find_most(column_name):\n' \
                    '    most = results[["ID", column_name, "Author", "Date created", "Message"]]\n' \
                    '    most = most.sort_values(by=[column_name], ascending=False)[:5].reset_index(drop=True)\n' \
                    '    most.index = most.index + 1\n' \
                    '    return most'

    reactions_subheader = '**a) Posts with the highest number of reactions:**\n\n' \
                          '<img src="https://github.com/IgorRosocha/FacebookPostsAnalysis/blob/master/' \
                          'FacebookPostsAnalysis/static/images/Reactions.png?raw=true" style="width: 400px;' \
                          ' float: left;"/>'
    most_reactions = 'find_most("Number of reactions")'

    likes_subheader = '**b) Posts with the highest number of likes:**\n\n' \
                      '<img src="https://github.com/IgorRosocha/FacebookPostsAnalysis/blob/master/' \
                      'FacebookPostsAnalysis/static/images/Like.png?raw=true" style="width: 400px; float: left;"/>'
    most_likes = 'find_most("Number of Likes")'

    shares_subheader = '**c) Posts with the highest number of shares:**\n\n' \
                       '<img src="https://github.com/IgorRosocha/FacebookPostsAnalysis/blob/master/' \
                       'FacebookPostsAnalysis/static/images/Share.png?raw=true" style="width: 400px; float: left;"/>'
    most_shares = 'find_most("Number of shares")'

    comments_subheader = '**d) Posts with the highest number of comments:**\n\n' \
                         '<img src="https://github.com/IgorRosocha/FacebookPostsAnalysis/blob/master/' \
                         'FacebookPostsAnalysis/static/images/Comment.png?raw=true" style="width: 400px;' \
                         ' float: left;"/>'
    most_comments = 'find_most("Number of comments")'

    unpopular_header = '### 2. Most unpopular posts:'

    angrys_subheader = '**a) Posts with the highest number of ANGRY reactions:**\n\n' \
                       '<img src="https://github.com/IgorRosocha/FacebookPostsAnalysis/blob/master/' \
                       'FacebookPostsAnalysis/static/images/Angry.png?raw=true" style="width: 400px; float: left;"/>'
    most_angrys = 'find_most("Number of Angrys")'

    sads_subheader = '**b) Posts with the highest number of SAD reactions:**\n\n' \
                     '<img src="https://github.com/IgorRosocha/FacebookPostsAnalysis/blob/master/' \
                     'FacebookPostsAnalysis/static/images/Sad.png?raw=true" style="width: 400px; float: left;"/>'
    most_sads = 'find_most("Number of Sads")'

    months_header = '### 3. Months with the biggest activity'

    biggest_activity = 'activity = results[["Number of reactions", "Number of comments", "Date created"]]\n' \
                       'activity = activity.assign(Ratio=activity["Number of reactions"] + ' \
                       'activity["Number of comments"])\n' \
                       'activity["Date created"] = pd.to_datetime(activity["Date created"])\n' \
                       'activity = activity.sort_values(by="Date created")\n' \
                       'activity["mnth_yr"] = activity["Date created"].apply(lambda x: x.strftime("%b-%Y"))\n' \
                       'activity = activity.groupby(["mnth_yr"], sort=False).sum()\n' \
                       'activity = activity.drop(["Number of comments", "Number of reactions"], 1)'

    graph = 'if activity["Ratio"].max() < 250:\n' \
            '    ticks = 10\n' \
            'elif activity["Ratio"].max() < 2500:\n' \
            '    ticks = 100\n' \
            'else:\n' \
            '    ticks = 1000\n\n' \
            'graph = activity.plot.bar(color="#8b9dc3", title="Months with the biggest activity", ' \
            'figsize=(15,5), legend=True)\n' \
            'graph.set_xlabel("Month")\n' \
            'graph.set_ylabel("Activity Ratio")\n' \
            'graph.yaxis.set_ticks(np.arange(0,activity["Ratio"].max(),ticks))\n' \
            'graph.set_facecolor("#f7f7f7")\n' \
            'graph.grid("on", which="major", axis="y")'

    nb['cells'] = [nbf.v4.new_markdown_cell(header),
                   nbf.v4.new_markdown_cell(images),
                   nbf.v4.new_code_cell(imports),
                   nbf.v4.new_markdown_cell(number_header),
                   nbf.v4.new_code_cell(number_of_posts),
                   nbf.v4.new_markdown_cell(popular_header),
                   nbf.v4.new_code_cell(popular_posts),
                   nbf.v4.new_markdown_cell(reactions_subheader),
                   nbf.v4.new_code_cell(most_reactions),
                   nbf.v4.new_markdown_cell(likes_subheader),
                   nbf.v4.new_code_cell(most_likes),
                   nbf.v4.new_markdown_cell(shares_subheader),
                   nbf.v4.new_code_cell(most_shares),
                   nbf.v4.new_markdown_cell(comments_subheader),
                   nbf.v4.new_code_cell(most_comments),
                   nbf.v4.new_markdown_cell(unpopular_header),
                   nbf.v4.new_markdown_cell(angrys_subheader),
                   nbf.v4.new_code_cell(most_angrys),
                   nbf.v4.new_markdown_cell(sads_subheader),
                   nbf.v4.new_code_cell(most_sads),
                   nbf.v4.new_markdown_cell(months_header),
                   nbf.v4.new_code_cell(biggest_activity),
                   nbf.v4.new_code_cell(graph)]

    notebook_name = 'analysis_' + entity_id + '.ipynb'

    with open(notebook_name, 'w') as f:
        nbf.write(nb, f)
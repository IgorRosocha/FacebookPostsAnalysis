import requests
import click
import configparser
import datetime
import csv
import nbformat as nbf
import time
from FacebookPostsAnalysis.notebook import create_notebook


def create_request(url, session):
    """
    Create a Facebook request and return the json.

    :param url: URL of Facebook group/page
    :param session: Facebook session
    """
    r = session.get(url)
    if r.status_code == 404:
        click.echo('Facebook: ERROR 404 - Not Found')
        exit(5)

    if r.status_code == 401:
        click.echo('Facebook: ERROR 401 - Bad credentials')
        exit(4)

    if r.status_code != 200:
        exit(10)

    return r.json()


def read_config(ctx):
    """
    Read the credentials and ID of Facebook group/page from configuration file.

    :param ctx: Context, which is automatically passed by Click library
    """
    config = ctx.obj['config']
    config_file = configparser.ConfigParser()

    if not config_file.read(config):
        click.echo("Configuration file not found!")
        exit(3)

    if config_file.has_option('credentials', 'app_id'):
        app_id = config_file['credentials']['app_id']
    else:
        print('No Facebook APP ID has been provided! Please fill in the APP ID in your configuration file!')
        exit(10)

    if config_file.has_option('credentials', 'app_secret'):
        app_secret = config_file['credentials']['app_secret']
    else:
        print('No Facebook APP SECRET has been provided! Please fill in the APP SECRET in your configuration file!')
        exit(10)

    entity = ctx.obj['entity']

    if entity == 'group':
        if config_file.has_option('facebook', 'group_id'):
            group_id = config_file['facebook']['group_id']
            page_id = ''
        else:
            print('No Facebook GROUP ID has been provided! Please fill in the GROUP ID in your configuration file!')
            exit(10)

    if entity == 'page':
        if config_file.has_option('facebook', 'page_id'):
            page_id = config_file['facebook']['page_id']
            group_id = ''
        else:
            print('No Facebook PAGE ID has been provided! Please fill in the PAGE ID in your configuration file!')
            exit(10)

    return app_id, app_secret, group_id, page_id


def build_token(app_id, app_secret):
    """
    Build a Facebook access token from your APP ID and APP SECRET.

    :param app_id: Your Facebook APP ID
    :param app_secret: Your Facebook APP SECRET
    """
    token = app_id + '|' + app_secret
    return token


def build_url_group(group_id, access_token, since_date, until_date, paging):
    """
    Build url of a Facebook group.

    :param group_id: ID of Facebook group
    :param access_token: Your Facebook access token
    :param since_date: Date since when to analyse Facebook posts
    :param until_date: Date until when to analyse Facebook posts
    :param paging: Paging token
    """
    url = "https://graph.facebook.com/v2.11/{}/feed".format(group_id) +\
          "/?limit={}&access_token={}".format(100, access_token) +\
          "&since={}".format(since_date) +\
          "&until={}".format(until_date) +\
          "&__paging_token={}".format(paging) + \
          "&fields=message,created_time,name,id," +\
          "comments.limit(0).summary(true),shares,reactions" +\
          ".limit(0).summary(true),from"
    return url


def build_url_page(page_id, access_token, paging, since_date, until_date):
    """
    Build url of a Facebook page.

    :param page_id: ID of Facebook page
    :param access_token: Your Facebook access token
    :param since_date: Date since when to analyse Facebook posts
    :param until_date: Date until when to analyse Facebook posts
    :param paging: Paging token
    """
    url = "https://graph.facebook.com/v2.11/{}/feed".format(page_id) +\
          "/?limit={}&access_token={}".format(100, access_token) + \
          "&after={}".format(paging) +\
          "&since={}".format(since_date) +\
          "&until={}".format(until_date) + \
          "&fields=message,created_time,name,id," +\
          "comments.limit(0).summary(true),shares,reactions" +\
          ".limit(0).summary(true),from"
    return url


def get_reactions(url, session):
    """
    Get the count of unique reactions of Facebook post.

    :param url: URL of Facebook group/page
    :param session: Facebook session
    """
    reactions = ['LIKE', 'LOVE', 'HAHA', 'WOW', 'SAD', 'ANGRY']
    reactions_count = {}

    for reaction in reactions:
        reactions_url = url + "&fields=reactions.type({}).limit(0).summary(total_count)".format(reaction)
        data = create_request(reactions_url, session)['data']

        dataset = set()
        for post in data:
            post_id = post['id']
            count = post['reactions']['summary']['total_count']
            dataset.add((post_id, count))

        for post_id, count in dataset:
            if post_id in reactions_count:
                reactions_count[post_id] = reactions_count[post_id] + (count,)
            else:
                reactions_count[post_id] = (count,)

    return reactions_count


def process_time(start_time):
    """
    Format the process time of analysis.

    :param start_time: Time when the analysis have started
    """
    seconds = time.time() - start_time
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return h, m, s


def print_version(ctx, param, value):
    """Print version of the app (default click implementation).

    :param ctx: Context, which is automatically passed by Click library
    :param param: Version parameter
    :param value: Version value
    """
    if not value or ctx.resilient_parsing:
        return
    click.echo('FacebookPostsAnalysis, version 0.1')
    ctx.exit()


@click.group('facebookpostsanalysis')
@click.option('-c', '--config', default='./config.cfg',
              help='Path to the config containing the credentials and Facebook group/page ID.')
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True, help="Show the version and exit.")
@click.pass_context
def cli(ctx, config):
    session = ctx.obj.get('session', requests.Session())
    ctx.obj['session'] = session
    ctx.obj['config'] = config


@cli.command(help='Get posts of the specified group/page.')
@click.argument('entity', nargs=1, type=click.Choice(['group', 'page']))
@click.option('--until', default='',
              help='Date until when to analyse Facebook posts.')
@click.option('--since', default='',
              help='Date since when to analyse Facebook posts.')
@click.option('--year', default='',
              help='Year to analyse Facebook posts.')
@click.pass_context
def get_posts(ctx, entity, **configuration):
    ctx.obj['entity'] = entity

    session = ctx.obj['session']
    until_date = configuration['until']
    since_date = configuration['since']
    year = configuration['year']

    paging = ''
    next_page = True

    csv_id = 0
    progress = 0
    now = datetime.datetime.now()

    config_credentials = read_config(ctx)
    token = build_token(config_credentials[0], config_credentials[1])

    start_time = time.time()
    print('FacebookPostsAnalysis v0.1')

    if year != '':
        if int(year) < 2004:
            print('[WRONG YEAR] Facebook has been launched in 2004!')
            exit(10)
        elif int(year) > now.year:
            print('[WRONG YEAR] It`s only year {} at the moment!'.format(now.year))
            exit(10)
        else:
            since_date = str(year) + '-01-01'
            until_date = str(year) + '-12-31'

    if since_date != '' and until_date != '':
        print('Analyzing posts since {} until {}.'.format(since_date, until_date))
    elif since_date != '' and until_date == '':
        print('Analyzing posts since {} until {}.'.format(since_date, now.strftime('%Y-%m-%d')))
    elif since_date == '' and until_date != '':
        print('Analyzing posts until {}.'.format(until_date))
    else:
        print('Analyzing posts until {}.'.format(now.strftime('%Y-%m-%d')))

    if entity == 'group':
        csv_name = 'analysis_csv_{}.csv'.format(config_credentials[2])
    elif entity == 'page':
        csv_name = 'analysis_csv_{}.csv'.format(config_credentials[3])

    with open(csv_name, 'w') as csvfile:
        fieldnames = ['ID', 'Message', 'Date created', 'Author',
                      'Number of reactions', 'Number of Likes', 'Number of Loves',
                      'Number of Hahas', 'Number of Wows', 'Number of Sads',
                      'Number of Angrys', 'Number of comments', 'Number of shares']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        while next_page:
            if entity == 'group':
                url = build_url_group(config_credentials[2], token, since_date, until_date, paging)
            elif entity == 'page':
                url = build_url_page(config_credentials[3], token, paging, since_date, until_date)

            posts = create_request(url, session)
            reactions = get_reactions(url, session)

            for post in posts['data']:
                post_id = post['id']

                if 'message' in post:
                    post_message = post['message']
                else:
                    post_message = '[MULTIMEDIA CONTENT] No message.'

                post_created = datetime.datetime.strptime(post['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
                post_created = post_created + datetime.timedelta(hours=+1)  # timezone fix
                post_created = post_created.strftime('%Y-%m-%d %H:%M:%S')  # convert back to string because of csv

                if 'from' in post:
                    post_author = post['from']['name']
                else:
                    post_author = 'Author unavailable.'

                if 'reactions' in post:
                    post_reactions = post['reactions']['summary']['total_count']
                else:
                    post_reactions = 0

                if 'comments' in post:
                    post_comments = post['comments']['summary']['total_count']
                else:
                    post_comments = 0

                if 'shares' in post:
                    post_shares = post['shares']['count']
                else:
                    post_shares = 0

                reactions_data = reactions[post_id]

                writer.writerow({'ID': csv_id, 'Message': post_message, 'Date created': post_created,
                                 'Author': post_author, 'Number of reactions': post_reactions,
                                 'Number of Likes': reactions_data[0], 'Number of Loves': reactions_data[1],
                                 'Number of Hahas': reactions_data[2], 'Number of Wows': reactions_data[3],
                                 'Number of Sads': reactions_data[4], 'Number of Angrys': reactions_data[5],
                                 'Number of comments': post_comments, 'Number of shares': post_shares})

                progress += 1
                if progress % 100 == 0:
                    print('[PROGRESS]: {} posts analyzed successfully!'.format(progress))

                csv_id += 1

            if 'paging' in posts:
                if entity == 'group':
                    next_url = posts['paging']['next']
                    until_date = next_url[next_url.index('until=') + len('until='):next_url.index('&__paging_token=')]
                    paging = next_url[next_url.index('paging_token=') + len('paging_token='):]
                elif entity == 'page':
                    paging = posts['paging']['cursors']['after']
            else:
                next_page = False

    if entity == 'group':
        create_notebook(config_credentials[2])
    elif entity == 'page':
        create_notebook(config_credentials[3])

    formatted_time = process_time(start_time)
    print('\nFacebookPostsAnalysis has finished the analysis!\n'
          '[RESULT] {} posts were successfully analyzed!\n'.format(progress) +
          'Process time: %d:%02d:%02d\n\n' % (formatted_time[0], formatted_time[1], formatted_time[2]) +
          'To see the results, open respective Notebook using Jupyter!\n'
          'For more information, please check the documentation or visit '
          'https://github.com/IgorRosocha/FacebookPostsAnalysis!')


def main():
    """
    Main function to run the cli.

    """
    cli(obj={})

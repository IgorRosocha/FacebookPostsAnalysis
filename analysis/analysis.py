import requests
import click
import configparser
import datetime
import csv


def create_request(url, session):
    """Create a request and return the json."""
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
    config = ctx.obj['config']
    config_file = configparser.ConfigParser()

    if not config_file.read(config):
        click.echo("Configuration file not found!")
        exit(3)

    app_id = config_file['credentials']['app_id']
    app_secret = config_file['credentials']['app_secret']
    group_id = config_file['facebook']['group_id']
    page_id = config_file['facebook']['page_id']

    return app_id, app_secret, group_id, page_id


def build_token(app_id, app_secret):
    token = app_id + '|' + app_secret
    return token


def build_url_group(group_id, access_token, since_date, until_date, paging):
    url = "https://graph.facebook.com/v2.9/{}/feed".format(group_id) +\
          "/?limit={}&access_token={}".format(100, access_token) +\
          "&since={}".format(since_date) +\
          "&until={}".format(until_date) +\
          "&__paging_token={}".format(paging) +\
          "&fields=message,created_time,name,id," +\
          "comments.limit(0).summary(true),shares,reactions" +\
          ".limit(0).summary(true),from"
    return url


def build_url_page(page_id, access_token, paging, since_date, until_date):
    url = "https://graph.facebook.com/v2.9/{}/feed".format(page_id) +\
          "/?limit={}&access_token={}".format(100, access_token) + \
          "&after={}".format(paging) +\
          "&since={}".format(since_date) +\
          "&until={}".format(until_date) +\
          "&fields=message,created_time,name,id," +\
          "comments.limit(0).summary(true),shares,reactions" +\
          ".limit(0).summary(true),from"
    return url


def print_version(ctx, param, value):
    """Print version of the app."""
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


@cli.command()
@click.argument('type', nargs=1, type=click.Choice(['group', 'page']))
@click.option('--until', default='',
              help='Date until when to analyse Facebook posts.')
@click.option('--since', default='',
              help='Date since when to analyse Facebook posts.')
@click.pass_context
def get_posts(ctx, type, **configuration):
    session = ctx.obj['session']
    until_date = configuration['until']
    since_date = configuration['since']
    paging = ''
    next_page = True

    config_credentials = read_config(ctx)
    token = build_token(config_credentials[0], config_credentials[1])

    with open('analysis.csv', 'w') as csvfile:
        fieldnames = ['ID', 'Message', 'Date created', 'Author',
                      'Number of reactions', 'Number of comments',
                      'Number of shares']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        while next_page:
            if type == 'group':
                url = build_url_group(config_credentials[2], token, since_date, until_date, paging)
            elif type == 'page':
                url = build_url_page(config_credentials[3], token, paging, since_date, until_date)

            posts = create_request(url, session)

            for post in posts['data']:
                post_id = post['id']

                if 'message' in post:
                    post_message = post['message']
                else:
                    post_message = 'No message.'

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

                writer.writerow({'ID': post_id, 'Message': post_message, 'Date created': post_created,
                                 'Author': post_author, 'Number of reactions': post_reactions,
                                 'Number of comments': post_comments, 'Number of shares': post_shares})

                print('ID: {0}\nMESSAGE: {1}\nCREATED: {2}\nAUTHOR: {3}\nREACTIONS: {4}\nCOMMENTS: {5}\nSHARES: {6}\n'
                      .format(post_id, post_message, post_created, post_author, post_reactions, post_comments, post_shares))

            if 'paging' in posts:
                if type == 'group':
                    next_url = posts['paging']['next']
                    until_date = next_url[next_url.index('until=') + len('until='):next_url.index('&__paging_token=')]
                    paging = next_url[next_url.index('paging_token=') + len('paging_token='):]
                elif type == 'page':
                    paging = posts['paging']['cursors']['after']
            else:
                next_page = False


if __name__ == '__main__':
    cli(obj={})

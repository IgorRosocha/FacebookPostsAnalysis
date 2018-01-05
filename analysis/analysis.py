import requests
import click


def create_request(url, session):
    """Create a request and return the json."""
    r = session.get(url)
    if r.status_code == 404:
        click.echo('GitHub: ERROR 404 - Not Found')
        exit(5)

    if r.status_code == 401:
        click.echo('GitHub: ERROR 401 - Bad credentials')
        exit(4)

    if r.status_code != 200:
        exit(10)

    return r.json()


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
@click.pass_context
def get_posts(ctx):
    print('get_posts method')


if __name__ == '__main__':
    cli(obj={})
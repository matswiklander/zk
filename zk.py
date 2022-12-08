import click

from zettel_linter_engine import ZettelLinterEngine
from zettel_repository import ZettelRepository
from zettel_search_engine import ZettelSearchEngine


def print_banner():
    banner = """               __    __         .__   __                     __                 
________ _____/  |__/  |_  ____ |  | |  | _______    _______/  |_  ____   ____  
\\___   // __ \\   __\\   __\\/ __ \\|  | |  |/ /\\__  \\  /  ___/\\   __\\/ __ \\ /    \\  v1.0
 /    /\\  ___/|  |  |  | \\  ___/|  |_|    <  / __ \\_\\___ \\  |  | \\  ___/|   |  \\
/_____ \\\\___  >__|  |__|  \\___  >____/__|_ \\(____  /____  > |__|  \\___  >___|  /
      \\/    \\/                \\/          \\/     \\/     \\/            \\/     \\/ """

    click.secho(banner, fg='cyan')


@click.group()
def cli():
    pass


@cli.command()
@click.argument('zettel_type', type=click.STRING)
def add(zettel_type: str):
    ZettelRepository().add(zettel_type)


@cli.group()
def search():
    pass


@search.command()
@click.argument('tags', nargs=-1)
@click.option("--summary", is_flag=True, show_default=True, default=False, help="Show summary of zettel")
def tags(tags, summary):
    ZettelSearchEngine(ZettelRepository()).search_tags(tags, summary)


@search.command()
@click.argument('texts', nargs=-1)
@click.option("--summary", is_flag=True, show_default=True, default=False, help="Show summary of zettel")
def text(texts, summary):
    ZettelSearchEngine(ZettelRepository()).search_text(texts, summary)


@cli.command()
def lint():
    ZettelLinterEngine(ZettelRepository()).lint()


@cli.command()
def stats():
    ZettelRepository().stats()


if __name__ == '__main__':
    print_banner()
    cli()

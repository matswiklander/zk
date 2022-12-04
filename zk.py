import click

from zettel_replacement_engine import ZettelReplacementEngine
from zettel_repository import ZettelRepository
from zettel_linter_engine import ZettelLinterEngine
from zettel_search_engine import ZettelSearchEngine


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
def tags(tags):
    ZettelSearchEngine(ZettelRepository()).search_tags(tags, True)


@search.command()
@click.argument('texts', nargs=-1)
def text(texts):
    ZettelSearchEngine(ZettelRepository()).search_text(texts, True)


@cli.command()
def lint():
    ZettelLinterEngine(ZettelRepository()).lint()


@cli.command()
def stats():
    ZettelRepository().stats()


if __name__ == '__main__':
    cli()

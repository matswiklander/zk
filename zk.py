import click

from zettel_repository import ZettelRepository
from zettel_linter import ZettelLinter
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
    zettel_repository = ZettelRepository()

    zettel_search_engine = ZettelSearchEngine(zettel_repository)

    zettel_search_engine.search_tags(tags, True)


@search.command()
@click.argument('texts', nargs=-1)
def text(texts):
    zettel_repository = ZettelRepository()

    zettel_search_engine = ZettelSearchEngine(zettel_repository)

    zettel_search_engine.search_text(texts, True)


@cli.command()
def lint():
    zettel_repository = ZettelRepository()

    zettel_linter = ZettelLinter(zettel_repository)

    zettel_linter.lint()


if __name__ == '__main__':
    cli()

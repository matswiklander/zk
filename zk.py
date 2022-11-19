import click

from engine import ZettelRepository, ZettelSearchEngine


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


if __name__ == '__main__':
    cli()

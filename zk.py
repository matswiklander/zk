import click

from zettel import ZettelRepository


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
    filtered_zettels = ZettelRepository().all_zettels

    for tag in tags:
        click.echo(tag)


if __name__ == '__main__':
    cli()

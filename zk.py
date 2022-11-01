import click

from functions import is_taken
from zettel import BaseZettel


@click.group()
def cli():
    pass


@cli.command()
@click.argument('zettel_type', type=click.STRING)
def add(zettel_type: str):
    try:
        zettel_class = \
            [zettel_class for zettel_class in BaseZettel.__subclasses__() if zettel_class.type == zettel_type][0]
    except IndexError:
        click.secho('Unknown zettel type, available zettel types:', fg='green')
        zettel_types = sorted([zettel_class.type for zettel_class in BaseZettel.__subclasses__()])
        click.secho('\n'.join(map(str, zettel_types)), fg='green')
        return

    zettel = zettel_class()

    if not is_taken(zettel.id):
        zettel.save()
    else:
        click.secho('ID already taken. Wait one minute before trying to create zettel again.', fg='green')


if __name__ == '__main__':
    cli()

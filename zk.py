import os

import click

from zettel import BaseZettel, is_taken, initiate_templates_directory


@click.group()
def cli():
    pass


@cli.command()
@click.argument('zettel_type', type=click.STRING)
def add(zettel_type: str):
    initiate_templates_directory()

    try:
        zettel_class = \
            [zettel_class for zettel_class in BaseZettel.__subclasses__() if
             zettel_class().mangled_name() == zettel_type][0]
    except IndexError:
        click.secho('Unknown zettel type, available zettel types are:', fg='green')
        zettel_types = sorted([zettel_class().mangled_name() for zettel_class in BaseZettel.__subclasses__()])
        click.secho('\n'.join(map(str, zettel_types)), fg='green')
        return

    zettel = zettel_class()

    if not is_taken(zettel.id):
        zettel.create()
        click.secho(
            '{} A new {}-zettel has been created'.format(os.sep.join([zettel.mangled_name(), zettel.id + '.md']),
                                                         zettel.mangled_name()), fg='green')
    else:
        click.secho('You can only create one new zettel every minute.', fg='yellow')


if __name__ == '__main__':
    cli()

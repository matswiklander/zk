import os

import click

from zettel import is_taken, initiate_templates_directory, zettel_factory


@click.group()
def cli():
    pass


@cli.command()
@click.argument('zettel_type', type=click.STRING)
def add(zettel_type: str):
    initiate_templates_directory()

    zettel = zettel_factory(zettel_type)

    if not is_taken(zettel.id):
        zettel.create()
        click.secho(
            '{} A new {}-zettel has been created'.format(os.sep.join([zettel.mangled_name(), zettel.id + '.md']),
                                                         zettel.mangled_name()), fg='green')
    else:
        click.secho('You can only create one new zettel every minute.', fg='yellow')


if __name__ == '__main__':
    cli()

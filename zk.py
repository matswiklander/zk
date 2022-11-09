import os

import click

from zettel import BaseZettel, is_taken


@click.group()
def cli():
    pass


@cli.command()
@click.argument('zettel_type', type=click.STRING)
def add(zettel_type: str):
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
    else:
        click.secho('You can only create one new zettel every minute.', fg='yellow')

    initiate_templates_directory()


def initiate_templates_directory():
    os.makedirs(os.sep.join([os.getcwd(), 'templates']), exist_ok=True)

    for zettel_class in BaseZettel.__subclasses__():
        with open(os.sep.join([os.getcwd(), 'templates', zettel_class().mangled_name() + '.md']), 'w',
                  encoding='utf-8') as fp:
            fp.write(zettel_class().template)


if __name__ == '__main__':
    cli()

import click


class Zettel:
    def __init__(self):
        pass


@click.group()
def cli():
    pass


@cli.command()
def new():
    pass


if __name__ == '__main__':
    cli()

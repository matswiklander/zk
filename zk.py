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


@cli.command()
@click.argument('type', type=click.STRING)
def add(type: str):
    click.secho(type, bg='red')
    pass


if __name__ == '__main__':
    cli()

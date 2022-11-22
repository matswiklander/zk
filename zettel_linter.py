import click

from zettel_repository import ZettelRepository


class ZettelLinter:
    def __init__(self, zettel_repository: ZettelRepository):
        self.zettel_repository = zettel_repository
        pass

    def lint(self):
        click.echo("Linting...")

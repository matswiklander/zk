import click

from zettel_repository import ZettelRepository
from zettel_linter_rules import fetch_all_zettel_linter_rules


class ZettelLinter:
    def __init__(self, zettel_repository: ZettelRepository):
        self.zettel_repository = zettel_repository
        pass

    def lint(self):
        all_zettel_linter_rules = fetch_all_zettel_linter_rules()
        all_zettels = self.zettel_repository.all_zettels

        click.echo(all_zettel_linter_rules)

        for zettel_linter_rule in all_zettel_linter_rules.values():
            all_zettels = [zettel for zettel in all_zettels if zettel_linter_rule().lint(zettel)]

        click.echo(self.__display_results(all_zettels, True))

    def __display_results(self, zettels, display_errors):
        click.clear()

        column_width = 0

        for zettel in zettels:
            width = len(zettel.path)
            if width > column_width:
                column_width = width

        if not len(zettels):
            click.secho('No results', fg='white')
            return

        for zettel in zettels:
            click.echo(click.style(zettel.path.ljust(column_width, ' '), fg='green') + ' ' +
                       click.style(zettel.title, fg='white'))

            if display_errors:
                click.echo('')

                for lint_error in zettel.lint_errors:
                    click.echo(' ' * column_width + ' ' + click.style(lint_error, fg='cyan'))

                click.echo('')

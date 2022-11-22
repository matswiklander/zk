import textwrap

import click

from zettel_repository import ZettelRepository


class ZettelSearchEngine:
    def __init__(self, zettel_repository: ZettelRepository):
        self.zettel_repository = zettel_repository
        pass

    def search_tags(self, tags, display_summary: bool):
        filtered_zettels = self.zettel_repository.all_zettels

        for tag in tags:
            filtered_zettels = [zettel for zettel in filtered_zettels if tag in zettel.tags]

        self.__display_search_results(filtered_zettels, display_summary)

    def search_text(self, texts, display_summary: bool):
        filtered_zettels = self.zettel_repository.all_zettels

        for text in texts:
            filtered_zettels = [zettel for zettel in filtered_zettels if
                                zettel.raw.lower().find(text.lower()) != -1]

        self.__display_search_results(filtered_zettels, display_summary)

    @staticmethod
    def __display_search_results(zettels, display_summary: bool):
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

            if display_summary:
                click.echo('')

                summary_lines = textwrap.wrap(zettel.summary, 80)

                for summary_line in summary_lines:
                    click.echo(' ' * column_width + ' ' + click.style(summary_line, fg='cyan'))

                click.echo('')

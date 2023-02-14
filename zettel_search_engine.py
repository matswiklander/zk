import os
import textwrap

import click

from common import get_terminal_width
from zettel_repository import ZettelRepository


class ZettelSearchEngine:
    def __init__(self, zettel_repository: ZettelRepository):
        self.zettel_repository = zettel_repository
        pass

    def search_tags(self, tags, display_summary: bool):
        filtered_zettels = self.zettel_repository.all_zettels_list

        and_tags = [tag for tag in tags if not tag.startswith('/')]
        not_tags = [tag[1:] for tag in tags if tag.startswith('/')]

        for tag in and_tags:
            filtered_zettels = [zettel for zettel in filtered_zettels if tag in zettel.tags]

        for tag in not_tags:
            filtered_zettels = [zettel for zettel in filtered_zettels if tag not in zettel.tags]

        self.__display_results(filtered_zettels, display_summary)

    def search_text(self, texts, display_summary: bool):
        filtered_zettels = self.zettel_repository.all_zettels_list

        for text in texts:
            filtered_zettels = [zettel for zettel in filtered_zettels if
                                zettel.raw.lower().find(text.lower()) != -1]

        self.__display_results(filtered_zettels, display_summary)

    @staticmethod
    def __display_results(zettels, display_summary: bool):
        terminal_width = get_terminal_width()
        link_column_width = 0

        if not len(zettels):
            return

        for zettel in zettels:
            width = len(zettel.path)
            if width > link_column_width:
                link_column_width = width

        title_and_summary_width = terminal_width - link_column_width - 1

        for zettel in zettels:
            title_lines = textwrap.wrap(zettel.title, title_and_summary_width)

            for index, title_line in enumerate(title_lines):
                if index == 0:
                    click.echo(
                        click.style(zettel.path.replace(os.sep, '/').rjust(link_column_width, ' '), fg='green') + ' ' +
                        click.style(title_line, fg='white'))
                else:
                    click.echo(' ' * link_column_width + ' ' +
                               click.style(title_line, fg='white'))

            if display_summary:
                click.echo()

                summary_lines = textwrap.wrap(zettel.summary, width=title_and_summary_width)

                for summary_line in summary_lines:
                    click.echo(' ' * link_column_width + ' ' + click.style(summary_line, fg='cyan'))

                click.echo()

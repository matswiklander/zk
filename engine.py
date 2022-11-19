import os
import re
from os.path import exists
import textwrap

import click

from zettel import BaseZettel


class ZettelRepository:
    def __init__(self):
        self.all_zettels = self.__load()
        self.__initiate_templates()

    def add(self, zettel_type):
        zettel = self.__zettel_factory(zettel_type)

        if not zettel:
            return

        if not self.__is_taken(zettel.id):
            zettel.create()
            click.secho('{} A new {}-zettel has been created'.format(os.sep.join([zettel.snake_case(),
                                                                                  zettel.id + '.md']),
                                                                     zettel.snake_case()), fg='green')
        else:
            click.secho('You can only create one new zettel every minute.', fg='yellow')

    def __load(self):
        all_zettels = []
        all_zettel_paths = self.__fetch_all_zettel_file_paths()

        for zettel_path in all_zettel_paths:
            all_zettels.append(BaseZettel().load(zettel_path))

        return all_zettels

    @staticmethod
    def __zettel_factory(zettel_type):
        try:
            zettel_class = [zettel_class for zettel_class in BaseZettel.__subclasses__() if
                            zettel_class().snake_case() == zettel_type][0]
        except IndexError:
            click.secho('Unknown zettel type, available zettel types are:', fg='green')
            zettel_types = sorted([zettel_class().snake_case() for zettel_class in BaseZettel.__subclasses__()])
            click.secho('\n'.join(map(str, zettel_types)), fg='green')
            return None

        zettel = zettel_class()
        return zettel

    @staticmethod
    def __initiate_templates():
        os.makedirs(os.sep.join([os.getcwd(), 'templates']), exist_ok=True)

        for zettel_class in BaseZettel.__subclasses__():
            template_path = os.sep.join([os.getcwd(), 'templates', zettel_class().snake_case() + '.md'])

            if not exists(template_path):
                with open(template_path, 'w', encoding='utf-8') as fp:
                    fp.write(zettel_class().template)

    @staticmethod
    def __fetch_all_zettel_file_paths():
        zettel_files = []
        for path, _, files in os.walk(os.getcwd()):
            for file in files:
                zettel_files.append(os.sep.join([path, file]))

        regex = re.compile(r'.+?(\d{12})\.md')

        zettel_files = [file for file in zettel_files if regex.search(file)]

        return zettel_files

    def __is_taken(self, zettel_id: str):
        zettel_file_paths = self.__fetch_all_zettel_file_paths()

        regex = re.compile(r'.+?(\d{12})\.md')

        zettel_file_paths = [regex.search(file).group(1) for file in zettel_file_paths if
                             regex.search(file).group(1) == zettel_id]

        if len(zettel_file_paths):
            return True

        return False


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

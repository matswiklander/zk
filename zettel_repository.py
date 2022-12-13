import os
import re
from collections import Counter
from os.path import exists

import click

from zettel_replacement_engine import ZettelReplacementEngine
from zettel_types import BaseZettel


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
            ZettelReplacementEngine().apply(zettel)
            zettel.save()

            click.echo(click.style('{}'.format(os.sep.join([zettel.path, zettel.id + '.md'])), fg='green') + ' ' +
                       click.style('A new {}-zettel has been created'.format(zettel.snake_case()), fg='white'))
        else:
            click.secho('You can only create one new zettel every minute.', fg='yellow')

    def stats_zettels(self):
        column_width = 0

        zettel_types = [zettel.snake_case() for zettel in self.all_zettels]
        zettel_type_occurrences = list(Counter(zettel_types).items())

        if not len(zettel_type_occurrences):
            return

        for zettel_type_occurrence in zettel_type_occurrences:
            width = len(zettel_type_occurrence[0])
            if width > column_width:
                column_width = width

        for zettel_type_occurrence in zettel_type_occurrences:
            click.echo(click.style(zettel_type_occurrence[0].ljust(column_width, ' '), fg='green') + ' ' +
                       click.style(zettel_type_occurrence[1], fg='white'))

    def stats_tags(self):
        column_width = 0

        all_zettel_tags = [tag for tags in [zettel.tags for zettel in self.all_zettels] for tag in tags]

        zettel_tag_occurrences = list(Counter(all_zettel_tags).items())

        if not len(zettel_tag_occurrences):
            return

        for zettel_tag_occurrence in zettel_tag_occurrences:
            width = len(zettel_tag_occurrence[0])
            if width > column_width:
                column_width = width

        for zettel_tag_occurrence in zettel_tag_occurrences:
            click.echo(click.style(zettel_tag_occurrence[0].ljust(column_width, ' '), fg='green') + ' ' +
                       click.style(zettel_tag_occurrence[1], fg='white'))

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

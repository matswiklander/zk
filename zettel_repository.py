import os
import re
from os.path import exists
from collections import Counter
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
            click.secho('{} A new {}-zettel has been created'.format(os.sep.join([zettel.snake_case(),
                                                                                  zettel.id + '.md']),
                                                                     zettel.snake_case()), fg='green')
        else:
            click.secho('You can only create one new zettel every minute.', fg='yellow')

    def stats(self):
        zettel_types = [zettel.snake_case() for zettel in self.all_zettels]
        zettel_type_occurrences = Counter(zettel_types).items()
        print(zettel_type_occurrences)

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

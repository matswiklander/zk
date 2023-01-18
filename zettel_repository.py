import math
import os
import re
import textwrap
from collections import Counter
from os.path import exists

import click

from zettel_replacement_engine import ZettelReplacementEngine
from zettel_types import BaseZettel, fetch_all_zettel_types


class ZettelRepository:
    def __init__(self):
        self.all_zettels_list, self.all_zettels_dict = self.__load()
        self.__initiate_templates()

    def add(self, zettel_type):
        zettel = self.__zettel_factory(zettel_type)

        if not zettel:
            return

        if not self.__is_taken(zettel.id):
            zettel.create()
            ZettelReplacementEngine().apply(zettel)
            zettel.save()

            click.echo(click.style(f'{zettel.path + os.sep + zettel.id + ".md"}', fg='green') + ' ' +
                       click.style(f'A new {zettel.snake_case()}-zettel has been created', fg='white'))
        else:
            click.secho('You can only create one new zettel every minute.', fg='yellow')

    def stats_zettels(self):
        zettel_types = [zettel.snake_case() for zettel in self.all_zettels_list]
        zettel_type_occurrences = sorted(list(Counter(zettel_types).items()), key=lambda tup: tup[0])

        if not len(zettel_type_occurrences):
            return

        self.__display_results(zettel_type_occurrences)

    def stats_tags(self):
        all_zettel_tags = [tag for tags in [zettel.tags for zettel in self.all_zettels_list] for tag in tags]

        all_zettel_types = list(fetch_all_zettel_types().keys())

        all_zettel_tags = [tag for tag in all_zettel_tags if tag not in all_zettel_types]

        zettel_tag_occurrences = sorted(list(Counter(all_zettel_tags).items()), key=lambda tup: tup[1], reverse=True)

        if not len(zettel_tag_occurrences):
            return

        self.__display_results(zettel_tag_occurrences)

    @staticmethod
    def __display_results(occurrences):
        OUTPUT_WIDTH = 80

        name_column_width = max([len(occurrence[0]) for occurrence in occurrences])
        occurrence_column_width = max([len(str(occurrence[1])) for occurrence in occurrences])
        number_of_columns_per_row = math.floor(OUTPUT_WIDTH / (name_column_width + occurrence_column_width + 2))

        click.secho('')

        for i, occurrence in enumerate(occurrences):
            click.secho(occurrence[0].rjust(name_column_width, ' '), fg='green', nl=False)
            click.secho(' ', nl=False)
            click.secho(str(occurrence[1]).ljust(occurrence_column_width, ' '), fg='white', nl=False)

            if not (i + 1) % number_of_columns_per_row:
                click.secho('')
            else:
                click.secho(' ', nl=False)

    def __load(self):
        all_zettels_list = []
        all_zettels_dict = {}
        all_zettel_paths = self.__fetch_all_zettel_file_paths()

        for zettel_path in all_zettel_paths:
            zettel = BaseZettel().load(zettel_path)
            all_zettels_list.append(zettel)
            all_zettels_dict[zettel.id] = zettel

        return all_zettels_list, all_zettels_dict

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

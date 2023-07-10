import math
import os
import re
from collections import Counter
from os.path import exists

import click

from common import get_terminal_width
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
        def split(list_a, chunk_size):
            for i in range(0, len(list_a), chunk_size):
                yield list_a[i:i + chunk_size]

        terminal_width = get_terminal_width()

        for i in reversed(range(1, terminal_width + 1)):
            names = list(split([occurrence[0] for occurrence in occurrences], i))
            try:
                names[-1] = names[-1] + [''] * (len(names[-2]) - len(names[-1]))
            except IndexError:
                pass

            names.append(['Total'])
            names[-1] = names[-1] + [''] * (len(names[-2]) - len(names[-1]))

            names_widths = [max(map(len, col)) for col in zip(*names)]

            count = list(split([str(occurrence[1]) for occurrence in occurrences], i))
            try:
                count[-1] = count[-1] + [''] * (len(count[-2]) - len(count[-1]))
            except IndexError:
                pass

            count.append([str(sum([occurrence[1] for occurrence in occurrences]))])
            count[-1] = count[-1] + [''] * (len(count[-2]) - len(count[-1]))

            count_widths = [max(map(len, col)) for col in zip(*count)]

            if i > len(names_widths):
                i = len(names_widths)

            overall_width = sum(names_widths) + sum(count_widths) + 2 * i + (i - 1)

            if overall_width < terminal_width:
                break

        indentation = math.floor((terminal_width - overall_width) / 2)

        click.secho()

        for i, row in enumerate(names):
            click.secho(' ' * indentation, nl=False)

            for j, name in enumerate(row):
                click.secho(name.rjust(names_widths[j], ' '), fg='green', nl=False)
                click.secho(' ', nl=False)
                click.secho(count[i][j].ljust(count_widths[j], ' '), fg='white', nl=False)
                click.secho('  ', nl=False)
            click.secho()
            if i == len(names) - 2:
                click.secho()

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

        regex = re.compile(r'.+?(\d{8}-\w{4})\.md')

        zettel_files = [file for file in zettel_files if regex.search(file)]

        return zettel_files

    def __is_taken(self, zettel_id: str):
        zettel_file_paths = self.__fetch_all_zettel_file_paths()

        regex = re.compile(r'.+?(\d{8}-\w{4})\.md')

        zettel_file_paths = [regex.search(file).group(1) for file in zettel_file_paths if
                             regex.search(file).group(1) == zettel_id]

        if len(zettel_file_paths):
            return True

        return False

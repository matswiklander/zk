import math
import os
import random
import re
import string
from datetime import datetime

import click
import toml
from dotenv import load_dotenv

from common import get_terminal_width
from zettel_repository import ZettelRepository

load_dotenv()


def print_banner():
    banner = r"""      (
      _)_           /777
     (o o)         (o o)
-ooO--(_)--Ooo-ooO--(_)--Ooo-
       patchwerk v1.1"""

    banner = banner.splitlines()

    terminal_width = get_terminal_width()

    banner_indent = math.floor((terminal_width - max([len(row) for row in banner])) / 2)

    if banner_indent < 0:
        banner = 'patchwerk v1.1'.splitlines()
        banner_indent = math.floor((terminal_width - max([len(row) for row in banner])) / 2)

    for row in banner:
        click.secho(' ' * banner_indent + row, fg='yellow', bold=True)


@click.group()
def cli():
    pass


@cli.command()
def patch():
    __create_missing_version_file()

    while True:
        version = __get_version()

        match version:
            case 1:
                __patch_001_002()
                break
            case 2:
                __patch_002_003()
                break


def __patch_001_002():
    zettels = __fetch_all_zettel_file_paths()

    regex = re.compile(r'.+?(\d{12}\.md)')

    old_filenames = []
    new_filenames = []

    for zettel in zettels:
        filename = regex.search(zettel).groups()[0]
        old_filenames.append(filename)

    for old_filename in old_filenames:
        new_filenames.append(__create_new_filename(old_filename))

    files_to_process = list(zip(zettels, old_filenames, new_filenames))

    for zettel in zettels:
        with open(zettel, 'r', encoding='utf-8') as input_file:
            content = input_file.read()
            for file_to_process in files_to_process:
                if file_to_process[1] in content:
                    old_filename = str(file_to_process[1])
                    new_filename = str(file_to_process[2])
                    content = content.replace(old_filename, new_filename)

            input_file.close()

            with open(zettel, 'w', encoding='utf-8') as output_file:
                output_file.write(content)

    for file_to_process in files_to_process:
        old_filename = str(file_to_process[1])
        new_filename = str(file_to_process[2])
        old_path = str(file_to_process[0])
        new_path = str(file_to_process[0]).replace(old_filename, new_filename)
        os.rename(old_path, new_path)

    __set_version(__get_version() + 1)


def __patch_002_003():
    zettels = ZettelRepository()

    for zettel in zettels.all_zettels_list:
        creation_date = datetime.strptime(f'{zettel.id[0:4]}-{zettel.id[4:6]}-{zettel.id[6:8]}', '%Y-%m-%d')
        zettel_front_matter = {'title': zettel.title, 'zettel_type': zettel.snake_case(),
                               'date': creation_date,
                               'tags': zettel.tags}
        content = '---\n'
        content += toml.dumps(zettel_front_matter)
        content += '---\n\n'
        content += zettel.summary
        content += '\n'
        content += zettel.body

        with open(zettel.path, 'w', encoding='utf-8') as fp:
            fp.write(content)

    __set_version(__get_version() + 1)


def __create_missing_version_file():
    if os.path.exists('./.VERSION') and os.path.isfile('./.VERSION'):
        return

    with open('./.VERSION', 'w') as version_file:
        version_file.write('1')


def __create_new_filename(old_filename) -> str:
    return old_filename[0:8] + '-' + ''.join(random.choices(string.ascii_lowercase, k=4)) + '.md'


def __get_version() -> int:
    with open('./.VERSION', 'r') as version_file:
        version = int(version_file.read())
        return version


def __set_version(version: int) -> None:
    with open('./.VERSION', 'w') as version_file:
        version_file.write(str(version))


def __fetch_all_zettel_file_paths():
    zettel_files = []
    for path, _, files in os.walk(os.getcwd()):
        for file in files:
            zettel_files.append(os.sep.join([path, file]))

    regex = re.compile(r'.+?(\d{12}\.md)')

    zettel_files = [file for file in zettel_files if regex.search(file)]

    return zettel_files


if __name__ == '__main__':
    print_banner()
    cli()

import os
import random
import re
import string
from datetime import datetime

import click
import requests
import toml
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

ZETTEL_TYPES = ['journal', 'link', 'note', 'todo']


class FrontMatter:
    def __init__(self):
        self.title = ''
        self.zettel_type = ''
        self.date = datetime.now()
        self.tags = []


class Zettel:
    def __init__(self, zettel_type: str):
        self.front_matter = FrontMatter()
        self.front_matter.zettel_type = zettel_type
        self.content = None
        self.path = None
        self.name = None

    def __str__(self):
        return_value = '---\n'
        return_value += toml.dumps(self.front_matter.__dict__)
        return_value += '---\n'
        return_value += str(self.content or '')

        return return_value

    def load(self, path: str, name: str):
        self.path = path
        self.name = name

        with open(self.path, 'r', encoding='utf-8') as fp:
            raw = fp.read()
            frontmatter = re.search(r'---(.+?)---', raw, re.DOTALL | re.MULTILINE).group(1).strip()

            self.front_matter = toml.loads(frontmatter)

            click.echo(self.front_matter)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('zettel_type', nargs=1, type=click.STRING)
@click.argument('params', nargs=-1)
def new(zettel_type: str, params: str):
    zettel = Zettel(zettel_type)

    match zettel_type:
        case 'journal':
            zettel = create_journal_zettel(params, zettel, zettel_type)
        case 'link':
            zettel = create_link_zettel(params, zettel, zettel_type)
        case 'note':
            zettel = create_note_zettel(params, zettel, zettel_type)
        case 'todo':
            zettel = create_todo_zettel(params, zettel, zettel_type)
        case other:
            click.echo(f'{other} is an unknown zettel type. Valid zettel types are: {valid_zettel_types()}')
            return

    save_zettel(zettel)


@cli.group()
def search():
    pass


@search.command()
@click.argument('tags', nargs=-1)
def tags(tags: str):
    not_tags = []
    and_tags = []
    for tag in tags:
        if tag[:1] == '/':
            not_tags.append(tag[1:])
        else:
            and_tags.append(tag)

    all_zettels = get_all_zettels()

    click.echo(and_tags)
    click.echo(not_tags)


def get_all_zettels():
    zettels_root_path = get_zettels_root_path()
    for dir_entry in os.scandir(zettels_root_path):
        zettel = Zettel('')
        zettel.load(dir_entry.path, dir_entry.name)


def save_zettel(zettel: Zettel):
    filename = datetime.now().strftime('%Y%m%d') + '-' + ''.join(random.choices(string.ascii_lowercase, k=4)) + '.md'
    zettels_root_path = get_zettels_root_path()

    if not os.path.exists(zettels_root_path):
        click.echo(f'{zettels_root_path} does not exist.')
        return

    with open(os.path.join(zettels_root_path, filename), 'w', encoding='utf-8') as fp:
        fp.write(str(zettel))


def get_zettels_root_path():
    return os.path.join(os.sep.join(os.path.split(os.environ['ZETTELS_ROOT_PATH'])), '', '')


def create_journal_zettel(_, zettel, zettel_type):
    match zettel_type:
        case 'journal':
            date = zettel.front_matter.date.strftime('%Y-%m-%d')
            zettel.front_matter.title = f'Journal {date}'
            zettel.front_matter.punch_in = '00:00'
            zettel.front_matter.punch_out = '00:00'
            zettel.content = '* [ ] ...'
        case _:
            zettel = None

    return zettel


def create_link_zettel(params, zettel, zettel_type):
    match zettel_type:
        case 'link' if params and len(params) > 1:
            title = get_link_title(params[0])
            zettel.front_matter.title = title

            for tag in params[1:]:
                if not tag in zettel.front_matter.tags:
                    zettel.front_matter.tags.append(tag)

            zettel.content = f'[{title}]({params[0]})'
        case _:
            zettel = None

    return zettel


def create_note_zettel(params, zettel, zettel_type):
    match zettel_type:
        case 'note' if params and len(params) == 1:
            zettel.front_matter.title = params[0]
        case 'note' if params and len(params) > 1:
            zettel.front_matter.title = params[0]

            for tag in params[1:]:
                if not tag in zettel.front_matter.tags:
                    zettel.front_matter.tags.append(tag)
        case _:
            zettel = None

    return zettel


def create_todo_zettel(params, zettel, zettel_type):
    match zettel_type:
        case 'todo' if params and len(params) == 1:
            zettel.front_matter.title = params[0]
            zettel.front_matter.tags.append = 'todo'
        case 'todo' if params and len(params) > 1:
            zettel.front_matter.title = params[0]

            for tag in params[1:]:
                if not tag in zettel.front_matter.tags:
                    zettel.front_matter.tags.append(tag)
        case _:
            zettel = None

    return zettel


def valid_zettel_types() -> str:
    return ', '.join(ZETTEL_TYPES)


def get_link_title(link: str) -> str:
    reqs = requests.get(link)

    soup = BeautifulSoup(reqs.text, 'html.parser')

    for title in soup.find_all('title'):
        return title.get_text()


if __name__ == '__main__':
    cli()

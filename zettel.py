import os
import re
from datetime import datetime
from os.path import exists

import click


def fetch_all_zettel_file_paths():
    zettel_files = []
    for path, subdirs, files in os.walk(os.getcwd()):
        for file in files:
            zettel_files.append(os.sep.join([path, file]))

    regex = re.compile(r'.+?(\d{12})(?:\.md)')

    zettel_files = [file for file in zettel_files if regex.search(file)]

    return zettel_files


def is_taken(zettel_id: str):
    zettel_file_paths = fetch_all_zettel_file_paths()

    regex = re.compile(r'.+?(\d{12})(?:\.md)')

    zettel_file_paths = [regex.search(file).group(1) for file in zettel_file_paths if
                         regex.search(file).group(1) == zettel_id]

    if len(zettel_file_paths):
        return True

    return False


def initiate_templates_directory():
    os.makedirs(os.sep.join([os.getcwd(), 'templates']), exist_ok=True)

    for zettel_class in BaseZettel.__subclasses__():
        template_path = os.sep.join([os.getcwd(), 'templates', zettel_class().mangled_name() + '.md'])

        if not exists(template_path):
            with open(template_path, 'w', encoding='utf-8') as fp:
                fp.write(zettel_class().template)


def zettel_factory(zettel_type):
    try:
        zettel_class = [zettel_class for zettel_class in BaseZettel.__subclasses__() if
                        zettel_class().mangled_name() == zettel_type][0]
    except IndexError:
        click.secho('Unknown zettel type, available zettel types are:', fg='green')
        zettel_types = sorted([zettel_class().mangled_name() for zettel_class in BaseZettel.__subclasses__()])
        click.secho('\n'.join(map(str, zettel_types)), fg='green')
        return None

    zettel = zettel_class()
    return zettel


class BaseZettel:
    template = None

    def __init__(self):
        self.id = self.__create_id()

    def create(self):
        os.makedirs(os.sep.join([os.getcwd(), self.mangled_name()]), exist_ok=True)

        with open(os.sep.join([os.getcwd(), self.mangled_name(), self.id + '.md']), 'w', encoding='utf-8') as out_fp:
            template = self.__fetch_template()
            out_fp.write(template)

    def mangled_name(self):
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', self.__class__.__name__[0:-6])
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    @staticmethod
    def __create_id():
        return datetime.now().strftime('%Y%m%d%H%M')

    def __extract_all_tags(self):
        pass

    def __fetch_template(self):
        with open(os.sep.join([os.getcwd(), 'templates', self.mangled_name() + '.md']), 'r',
                  encoding='utf-8') as template_fp:
            template = template_fp.read()

        return template


class LinkZettel(BaseZettel):
    template = '''# Link

[]()

---

Summary

---

§link
'''

    def __init__(self):
        super().__init__()


class JournalZettel(BaseZettel):
    template = '''# Journal

§journal
'''

    def __init__(self):
        super().__init__()


class NoteZettel(BaseZettel):
    template = '''# Note

§note
'''

    def __init__(self):
        super().__init__()


class MinutesZettel(BaseZettel):
    template = '''# Minutes

§minutes
'''

    def __init__(self):
        super().__init__()

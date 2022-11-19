import os
import re
from datetime import datetime
from os.path import exists

import click


def fetch_all_zettel_types():
    all_zettel_types = {zettel_class().snake_case(): zettel_class for zettel_class in BaseZettel.__subclasses__()}
    return all_zettel_types


class BaseZettel:
    template = None

    def __init__(self):
        self.id = self.__create_id()
        self.raw = ''
        self.title = ''
        self.summary = ''
        self.body = ''
        self.tags = []

    def create(self):
        os.makedirs(os.sep.join([os.getcwd(), self.snake_case()]), exist_ok=True)

        with open(os.sep.join([os.getcwd(), self.snake_case(), self.id + '.md']), 'w', encoding='utf-8') as out_fp:
            template = self.__fetch_template()
            out_fp.write(template)

    def load(self, zettel_path: str):
        with open(zettel_path, 'r', encoding='utf-8') as fp:
            self.raw = fp.read()

        self.tags = self.__extract_all_tags()

        # Extract title
        title = re.findall(r'# (.+)', self.raw)

        if len(title) != 0:
            self.title = title[0]
        else:
            self.title = 'Untitled'

        # Extract summary
        self.summary = re.search(r'---(.+?)---', self.raw, re.DOTALL | re.MULTILINE).group(0)

        # Extract body
        self.body = re.search(r'.*---(.+?)---', self.raw, re.DOTALL | re.MULTILINE).group(0)

        all_zettel_types = fetch_all_zettel_types()

        for tag in self.tags:
            if tag in all_zettel_types:
                self.__class__ = all_zettel_types[tag]
                return self

        self.__class__ = BaseZettel
        return self

    def snake_case(self):
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', self.__class__.__name__[0:-6])
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    @staticmethod
    def __create_id():
        return datetime.now().strftime('%Y%m%d%H%M')

    def __extract_all_tags(self):
        return list(dict.fromkeys(re.findall(r'§(\w+)', self.raw)))

    def __fetch_template(self):
        with open(os.sep.join([os.getcwd(), 'templates', self.snake_case() + '.md']), 'r',
                  encoding='utf-8') as template_fp:
            template = template_fp.read()

        return template


class ReferenceZettel(BaseZettel):
    template = '''# Reference

---

Summary

---

Body

---

§reference
'''

    def __init__(self):
        super().__init__()


class JournalZettel(BaseZettel):
    template = '''# Journal

---

Summary

---

Body

---

§journal
'''

    def __init__(self):
        super().__init__()


class NoteZettel(BaseZettel):
    template = '''# Note

---

Summary

---

Body

---

§note
'''

    def __init__(self):
        super().__init__()


class MinutesZettel(BaseZettel):
    template = '''# Minutes

---

Summary

---

Body

---

§minutes
'''

    def __init__(self):
        super().__init__()


class LinkZettel(BaseZettel):
    template = '''# Link

---

Summary

---

[]()

---

§link
'''

    def __init__(self):
        super().__init__()


class MermaidZettel(BaseZettel):
    template = '''# Mermaid

---

Summary

---

```mermaid
```

---

§mermaid
'''

    def __init__(self):
        super().__init__()


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
            click.secho(
                '{} A new {}-zettel has been created'.format(os.sep.join([zettel.snake_case(), zettel.id + '.md']),
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
    def __init__(self):
        pass

import os
import re
import random
import string
from datetime import datetime


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
        self.path = ''
        self.tags = []
        self.links = []
        self.lint_errors = []

    def create(self):
        self.raw = self.__fetch_template()

    def save(self):
        relative_zettel_path = os.sep.join([self.snake_case(), self.id[0:4], self.id[4:6]])
        full_zettel_path = os.sep.join([os.getcwd(), relative_zettel_path])

        self.path = relative_zettel_path

        os.makedirs(full_zettel_path, exist_ok=True)

        with open(os.sep.join([full_zettel_path, self.id + '.md']), 'w', encoding='utf-8', newline='\n') as out_fp:
            self.raw = '\n'.join(self.raw.splitlines()) + '\n'
            out_fp.write(self.raw)

    def load(self, zettel_path: str):
        with open(zettel_path, 'r', encoding='utf-8') as fp:
            self.raw = fp.read()

        self.path = zettel_path.replace(os.getcwd(), '')

        self.path = self.path[1:len(self.path)]

        self.__extract_id(zettel_path)
        self.__extract_title()
        self.__extract_summary()
        self.__extract_body()

        all_zettel_types = fetch_all_zettel_types()

        self.tags = self.__extract_all_tags()
        self.__extract_all_internal_links()

        # Cast self to correct type based on tag
        for tag in self.tags:
            if tag in all_zettel_types:
                self.__class__ = all_zettel_types[tag]
                return self

        self.__class__ = BaseZettel
        return self

    def __extract_body(self):
        # Extract body
        try:
            self.body = re.search(r'.*---(.+?)---', self.raw, re.DOTALL | re.MULTILINE).group(1).strip()
        except AttributeError:
            self.body = ''

    def __extract_summary(self):
        # Extract summary
        try:
            self.summary = re.search(r'---(.+?)---', self.raw, re.DOTALL | re.MULTILINE).group(1).strip()
        except AttributeError:
            self.summary = ''

    def __extract_title(self):
        # Extract title
        title = re.findall(r'# (.+)', self.raw)
        if len(title) != 0:
            self.title = title[0].strip()
        else:
            self.title = ''

    def __extract_id(self, zettel_path):
        # Extract id
        id = re.findall(r'.+?(\d{8}-\w{4})\.md', zettel_path)
        if len(id) != 0:
            self.id = id[0].strip()
        else:
            self.id = self.__create_id()

    def snake_case(self):
        name = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', self.__class__.__name__[0:-6])
        return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    @staticmethod
    def __create_id():
        return datetime.now().strftime('%Y%m%d') + '-' + ''.join(random.choices(string.ascii_lowercase, k=4))

    def __extract_all_tags(self):
        return [x.lower() for x in list(dict.fromkeys(re.findall(r'§([\w-]+)', self.raw)))]

    def __extract_all_internal_links(self):
        all_links = self.__extract_all_links()

        if len(all_links) == 0:
            return True

        for link in all_links:
            zettel_id = re.findall(r'.+?(\d{8}-\w{4})\.md', link[1])

            if len(zettel_id):
                self.links.append(zettel_id[0])

    def __extract_all_links(self):
        all_links = re.findall(r'\[(.+?)\]\((.+?)\)', self.raw, re.DOTALL | re.MULTILINE)
        return all_links

    def __fetch_template(self):
        with open(os.sep.join([os.getcwd(), 'templates', self.snake_case() + '.md']), 'r',
                  encoding='utf-8') as template_fp:
            template = template_fp.read()

        return template


class JournalZettel(BaseZettel):
    template = '''# Journal {{today}}

---

Summary

---

Body

---

§journal
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
        self.__extract_all_internal_links()

    def __extract_all_internal_links(self):
        pass
        # click.echo('Extracting link links')


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


class TodoZettel(BaseZettel):
    template = '''# Todo

---

Summary

---

Body

---

§todo
'''

    def __init__(self):
        super().__init__()

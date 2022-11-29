import os
import re
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
        self.lint_errors = []

    def create(self):
        os.makedirs(os.sep.join([os.getcwd(), self.snake_case()]), exist_ok=True)

        with open(os.sep.join([os.getcwd(), self.snake_case(), self.id + '.md']), 'w', encoding='utf-8') as out_fp:
            template = self.__fetch_template()
            out_fp.write(template)

    def load(self, zettel_path: str):
        with open(zettel_path, 'r', encoding='utf-8') as fp:
            self.raw = fp.read()

        self.path = zettel_path.replace(os.getcwd(), '')

        self.path = self.path[1:len(self.path)]

        # Extract title
        title = re.findall(r'# (.+)', self.raw)

        if len(title) != 0:
            self.title = title[0].strip()
        else:
            self.title = ''

        # Extract summary
        try:
            self.summary = re.search(r'---(.+?)---', self.raw, re.DOTALL | re.MULTILINE).group(1).strip()
        except AttributeError:
            self.summary = ''

        # Extract body
        try:
            self.body = re.search(r'.*---(.+?)---', self.raw, re.DOTALL | re.MULTILINE).group(1).strip()
        except AttributeError:
            self.body = ''

        all_zettel_types = fetch_all_zettel_types()

        self.tags = self.__extract_all_tags()

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
        return [x.lower() for x in list(dict.fromkeys(re.findall(r'§(\w+)', self.raw)))]

    def __fetch_template(self):
        with open(os.sep.join([os.getcwd(), 'templates', self.snake_case() + '.md']), 'r',
                  encoding='utf-8') as template_fp:
            template = template_fp.read()

        return template


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

import os
import re
from datetime import datetime


def is_taken(zettel_id: str):
    zettel_files = []
    for path, subdirs, files in os.walk(os.getcwd()):
        for name in files:
            zettel_files.append(name)

    regex = re.compile(r'(\d{12})(?:\.md)')

    zettel_files = [file for file in zettel_files if regex.search(file)]

    zettel_files = [regex.search(file).group(1) for file in zettel_files if regex.search(file).group(1) == zettel_id]

    if len(zettel_files):
        return True

    return False


class BaseZettel:
    template = None

    def __init__(self):
        self.id = self.__create_id()

    def create(self):
        os.makedirs(os.sep.join([os.getcwd(), self.mangled_name()]), exist_ok=True)

        with open(os.sep.join([os.getcwd(), self.mangled_name(), self.id + '.md']), 'w', encoding='utf-8') as out_fp:
            with open(os.sep.join([os.getcwd(), 'templates', self.mangled_name() + '.md']), 'r',
                      encoding='utf-8') as template_fp:
                template = template_fp.read()
                out_fp.write(template)

    def mangled_name(self):
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', self.__class__.__name__[0:-6])
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    @staticmethod
    def __create_id():
        return datetime.now().strftime('%Y%m%d%H%M')


class LinkZettel(BaseZettel):
    template = '''# Link
[]()

§link'''

    def __init__(self):
        super().__init__()


class JournalZettel(BaseZettel):
    template = '''# Journal
    
§journal'''

    def __init__(self):
        super().__init__()


class NoteZettel(BaseZettel):
    template = '''# Note
    
§note'''

    def __init__(self):
        super().__init__()


class MinutesZettel(BaseZettel):
    template = '''# Minutes

§minutes'''

    def __init__(self):
        super().__init__()

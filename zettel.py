import os
from datetime import datetime


class BaseZettel:
    path = None
    template = None
    type = 'base'

    def __init__(self):
        self.id = self.__create_id()

    def save(self):
        with open(os.getcwd() + os.sep + self.id + '.md', 'w', encoding='utf-8') as fp:
            fp.write('test')

    @staticmethod
    def __create_id():
        return datetime.now().strftime('%Y%m%d%H%M')


class LinkZettel(BaseZettel):
    path = 'links'
    template = '''Link'''
    type = 'link'

    def __init__(self):
        super().__init__()


class JournalZettel(BaseZettel):
    path = 'journal'
    template = '''Journal'''
    type = 'journal'

    def __init__(self):
        super().__init__()


class NoteZettel(BaseZettel):
    path = 'notes'
    template = '''Note'''
    type = 'note'

    def __init__(self):
        super().__init__()


class MinutesZettel(BaseZettel):
    path = 'minutes'
    template = '''Minutes'''
    type = 'minutes'

    def __init__(self):
        super().__init__()

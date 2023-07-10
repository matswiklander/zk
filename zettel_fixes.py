import re

from zettel_repository import ZettelRepository
from zettel_types import BaseZettel


def fetch_all_zettel_fixes():
    all_zettel_fixes = {zettel_fix_class().snake_case(): zettel_fix_class for zettel_fix_class in
                        BaseZettelFix.__subclasses__()}
    return all_zettel_fixes


class BaseZettelFix:
    def __init__(self):
        pass

    def snake_case(self):
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', self.__class__.__name__[0:-9])
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


class LinkTitleZettelFix(BaseZettelFix):
    def __init__(self):
        super().__init__()

    @staticmethod
    def fix(zettel: BaseZettel, zettel_repository: ZettelRepository):
        all_links = re.findall(r'\[([^][]+)\]\((.+?)\)', zettel.raw, re.DOTALL | re.MULTILINE)

        if len(all_links) == 0:
            return True

        for link in all_links:
            zettel_id = re.findall(r'.+?(\d{8}-\w{4})\.md', link[1])

            if len(zettel_id) and len(zettel_id[0]):
                try:
                    linked_zettel = zettel_repository.all_zettels_dict[zettel_id[0]]

                    zettel.raw = zettel.raw.replace(f'[{link[0]}]({link[1]})', f'[{linked_zettel.title}]({link[1]})')

                    zettel.save()

                except KeyError:
                    zettel.lint_errors.append('    ' + link[1] + ' => Missing')

        return True

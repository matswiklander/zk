import os
import re

from zettel_repository import ZettelRepository
from zettel_types import BaseZettel, fetch_all_zettel_types


def fetch_all_zettel_linter_rules():
    all_zettel_linter_rules = {zettel_linter_class().snake_case(): zettel_linter_class for zettel_linter_class in
                               BaseZettelLinterRule.__subclasses__()}
    return all_zettel_linter_rules


class BaseZettelLinterRule:
    def __init__(self):
        pass

    def snake_case(self):
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', self.__class__.__name__[0:-10])
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


class NoUnknownZettelLinterRule(BaseZettelLinterRule):
    def __init__(self):
        super().__init__()

    @staticmethod
    def lint(zettel: BaseZettel, zettel_repository: ZettelRepository):
        if type(zettel) == BaseZettel:
            zettel.lint_errors.append("No Zettel with unknown type allowed.")
            return True

        return False


class NoZettelWithoutTitleLinterRule(BaseZettelLinterRule):
    def __init__(self):
        super().__init__()

    @staticmethod
    def lint(zettel: BaseZettel, zettel_repository: ZettelRepository):
        if len(zettel.title.strip()) == 0:
            zettel.lint_errors.append("No Zettel without title allowed.")
            return True

        return False


class NoZettelWithoutSummaryLinterRule(BaseZettelLinterRule):
    def __init__(self):
        super().__init__()

    @staticmethod
    def lint(zettel: BaseZettel, zettel_repository: ZettelRepository):
        if len(zettel.summary.strip()) == 0:
            zettel.lint_errors.append("No Zettel without summary allowed.")
            return True

        return False


class NoZettelWithoutBodyLinterRule(BaseZettelLinterRule):
    def __init__(self):
        super().__init__()

    @staticmethod
    def lint(zettel: BaseZettel, zettel_repository: ZettelRepository):
        if len(zettel.body.strip()) == 0:
            zettel.lint_errors.append("No Zettel without body allowed.")
            return True

        return False


class NoAmbiguousZettelLinterRule(BaseZettelLinterRule):
    def __init__(self):
        super().__init__()

    @staticmethod
    def lint(zettel: BaseZettel, zettel_repository: ZettelRepository):
        all_zettel_types = fetch_all_zettel_types()

        found_zettel_types = [tag for tag in zettel.tags if tag in all_zettel_types]

        if len(found_zettel_types) > 1:
            zettel.lint_errors.append("No Zettel with ambiguous type allowed.")
            return True

        return False


class NoBrokenLinksInZettelLinterRule(BaseZettelLinterRule):
    def __init__(self):
        super().__init__()

    @staticmethod
    def lint(zettel: BaseZettel, zettel_repository: ZettelRepository):
        all_links = re.findall(r'\[(.+?)\]\((.+?)\)', zettel.raw, re.DOTALL | re.MULTILINE)

        if len(all_links) == 0:
            return False

        for link in all_links:
            zettel_id = re.findall(r'.+?(\d{8}-\w{4})\.md', link[1])

            if len(zettel_id) != 0:
                try:
                    linked_zettel = zettel_repository.all_zettels_dict[zettel_id[0]]

                    if not linked_zettel.path.replace(os.sep, '/') in link[1]:
                        zettel.lint_errors.append('    ' + link[1] + ' => /' + linked_zettel.path.replace(os.sep, '/'))

                except KeyError:
                    zettel.lint_errors.append('    ' + link[1] + ' => Missing')

        if len(zettel.lint_errors):
            zettel.lint_errors.insert(0, "No Zettel with broken internal links allowed.")

        return False


MAX_TAG_LENGTH = 20


class NoOverlongTagsInZettelLinterRule(BaseZettelLinterRule):
    def __init__(self):
        super().__init__()

    @staticmethod
    def lint(zettel: BaseZettel, zettel_repository: ZettelRepository):
        for tag in zettel.tags:
            if len(tag) > MAX_TAG_LENGTH:
                zettel.lint_errors.append(f'    §{tag} is longer than {MAX_TAG_LENGTH}')

        if len(zettel.lint_errors):
            zettel.lint_errors.insert(0, "No Zettel with overlong tags allowed.")

        return False

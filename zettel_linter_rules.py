import re

from zettel_types import BaseZettel


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
        pass

    @staticmethod
    def lint(zettel: BaseZettel):
        if type(zettel) == BaseZettel:
            zettel.lint_errors.append("No Unknown Zettel allowed. Check the tags.")
            return True

        return False

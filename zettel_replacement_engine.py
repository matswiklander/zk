import click

from zettel_replacement_types import fetch_all_zettel_replacement_types
from zettel_types import BaseZettel


class ZettelReplacementEngine:
    def __init__(self):
        pass

    @staticmethod
    def apply(zettel: BaseZettel):
        all_zettel_replacement_types = fetch_all_zettel_replacement_types()

        for zettel_replacement in all_zettel_replacement_types.values():
            zettel_replacement().apply(zettel)

from zettel_fixes import fetch_all_zettel_fixes
from zettel_repository import ZettelRepository


class ZettelFixEngine:
    def __init__(self, zettel_repository: ZettelRepository):
        self.zettel_repository = zettel_repository
        pass

    def fix(self):
        all_zettel_fix_rules = fetch_all_zettel_fixes()
        all_zettels = self.zettel_repository.all_zettels_list

        for zettel_fix in all_zettel_fix_rules.values():
            for zettel in all_zettels:
                zettel_fix().fix(zettel, self.zettel_repository)

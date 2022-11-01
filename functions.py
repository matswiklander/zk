import os
import re


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

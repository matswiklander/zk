import os


def get_terminal_width():
    try:
        (terminal_width, _) = os.get_terminal_size()
    except OSError:
        return 80

    return terminal_width

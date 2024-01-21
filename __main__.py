import sys

from books import digest as digest_books
from increlance.self import Self
import types

def run():
    self = Self(sys.argv[1] if len(sys.argv) > 1 else 'Increlance')
    # TODO self.run()


def __main__():
    if len(sys.argv) > 1 and sys.argv[1] == '--comprehend':
        digest_books()
        return

    run()


if __name__ == "__main__":
    __main__()

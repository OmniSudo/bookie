import sys

from books import digest as digest_books
from tracy.root import Root
import types

def do():
    Root().do(None)


def __main__():
    if len(sys.argv) > 1 and sys.argv[1] == '--comprehend':
        digest_books()
        return

    do()


if __name__ == "__main__":
    __main__()

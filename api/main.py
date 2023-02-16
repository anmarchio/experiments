import argparse
import os
import sys

from importing import import_one, import_many


def main():
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-io", "--importone", help="imports single result dir")
    argParser.add_argument("-im", "--importmany", help="import list of result dirs")
    args = argParser.parse_args()

    if args.importone is not None:
        import_one(args.importone)
    elif args.importmany is not None:
        import_many(args.importmany)

    sys.exit()


if __name__ == '__main__':
    main()

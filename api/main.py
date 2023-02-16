import argparse
import os
import sys

from importing import import_one, import_many

PATH = os.path.join("C:\\", "dev", "experiments", "scripts", "results", "202302010706")


def main():
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-io", "--importone", help="imports single result dir")
    argParser.add_argument("-im", "--importmany", help="import list of result dirs")
    args = argParser.parse_args()

    test_path = [
        "C:\\dev\\experiments\\test_api\\results\\202302010706",
        "C:\\dev\experiments\\test_api\\results\\202301010001_excpt",
        "C:\\dev\experiments\\test_api\\results\\202301010003_incompl",
        "C:\\dev\experiments\\test_api\\results\\202301010002_empty"
    ]
    import_one(test_path[0])
    """
    if args.importone != "":
        import_one(args.importone)
    elif args.importmany != "":
        import_many(args.importmany)
    """
    #if DEV_MODE:
    #    DB.delete_session()
    #    if os.path.exists(SQLITE_PATH):
    #        os.remove(SQLITE_PATH)

    sys.exit()


if __name__ == '__main__':
    main()

import os

from api.importing import import_one

PATH = os.path.join("C:\\", "dev", "experiments", "scripts", "results", "202302010706")


def main():
    import_one(PATH)


if __name__ == '__main__':
    main()

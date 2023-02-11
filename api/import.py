def import_one(path: str):
    """
    reads data from cgp optimization experiment
    and translates them to python model objects
    """
    print('Importing %s', path)
    pass


def import_many(paths: []):
    """
    reads list of data containing
    cgp optimization experiments
    """
    for path in paths:
        import_one(path)
    print('Done importing.')
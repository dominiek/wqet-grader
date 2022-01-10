import os

my_dir = os.path.dirname(os.path.abspath(__file__))


def fixture_path(path):
    return os.path.join(my_dir, "../fixtures/", path)

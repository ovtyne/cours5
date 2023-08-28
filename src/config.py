import pathlib
from configparser import ConfigParser

PATH_TO_CONFIG = pathlib.Path(pathlib.Path.cwd(), '', 'database.ini')


def config():
    parser = ConfigParser()
    parser.read(PATH_TO_CONFIG)
    db = {}
    if parser.has_section("postgresql"):
        params = parser.items("postgresql")
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format("postgresql", PATH_TO_CONFIG))
    return db


import os
import unittest

from api.importing import import_one
from test_api.setup import setup_database


class TestImport(unittest.TestCase):
    def setUp(self) -> None:
        self.session = setup_database()

        self.test_paths = {
            "regular": os.path.join("test_api", "results","202302010706"),
            "exception_only": os.path.join("test_api", "results","202301010001_excpt"),
            "missing_runs": os.path.join("test_api", "results","202301010003_incompl"),
            "empty_runs": os.path.join("test_api", "results","202301010002_empty")
        }

    def test_regular(self):
        import_one(self.test_paths["regular"])

    def test_exception_only(self):
        import_one(self.test_paths["exception_only"])

    def test_missing_runs(self):
        import_one(self.test_paths["missing_runs"])

    def test_empty_runs(self):
        import_one(self.test_paths["empty_runs"])

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()

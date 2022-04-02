import os
import unittest
import importlib.util
from sqllex.constants import *
from sqllex.classes import SQLite3x

# from sqllex.debug import debug_mode
# debug_mode(True)


def save_prof(func: callable):
    def wrapper(*args, **kwargs):
        import pstats
        import cProfile

        with cProfile.Profile() as pr:
            func(*args, **kwargs)

        stat = pstats.Stats(pr)
        stat.sort_stats(pstats.SortKey.TIME)
        stat.dump_stats(filename=f'sqlite_time_{func.__name__}.prof')

    return wrapper


# @unittest.skip("Turned off manually")
@unittest.skipUnless(importlib.util.find_spec('cProfile'), "Module cProfile not found")
@unittest.skipUnless(importlib.util.find_spec('pstats'), "Module pstats not found")
class TimeTestsSqllexSQLite(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.complexity = 1000
        cls.db_name = f"test_sqllex_db"
        cls.db = SQLite3x(path=cls.db_name)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.db.disconnect()
        os.remove(cls.db_name)

    @save_prof
    def test_create_table(self):
        self.db.create_table(
            'main',
            {
                'id': [INTEGER, PRIMARY_KEY, UNIQUE],
                'name': [TEXT],
                'age': [INTEGER, DEFAULT, 33]
            }
        )

    @save_prof
    def test_insert_fast(self):
        for _ in range(self.complexity):
            self.db.insert('main', (None, f'Alex', 33))

    @save_prof
    def test_insert_slow(self):
        for _ in range(self.complexity):
            self.db.insert('main', (None, 'Alex'))

    @save_prof
    def test_insert_many_fast(self):
        data = [(None, 'Alex', 33) for _ in range(self.complexity)]

        self.db.insertmany('main', data)

    @save_prof
    def test_insert_many_slow(self):
        data = [(None, 'Alex') for _ in range(self.complexity)]

        self.db.insertmany('main', data)

    @save_prof
    def test_select_all(self):
        self.db.select_all('main', LIMIT=self.complexity)

    @save_prof
    def test_select_where_1(self):
        """
        Select where (something)
        """
        self.db.select(
            'main', 'id',
            WHERE={
                'name': 'Alex'
            },
            LIMIT=self.complexity
        )

    @save_prof
    def test_select_where_2(self):
        """
        Modern new way for WHERE (SearchConditions)
        """
        main_tab = self.db['main']
        id_col = main_tab['id']
        name_col = main_tab['name']

        self.db.select(
            main_tab, id_col,
            WHERE=(name_col == 'Alex'),
            LIMIT=self.complexity
        )


if __name__ == '__main__':
    unittest.main()

import unittest
import importlib.util
from sqllex.constants import *
from sqllex.constants.postgresql import *
from sqllex.classes import PostgreSQLx
import psycopg2

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
        stat.dump_stats(filename=f'time_{func.__name__}.prof')

    return wrapper


# @unittest.skip("Turned off manually")
@unittest.skipUnless(importlib.util.find_spec('cProfile'), "Module cProfile not found")
@unittest.skipUnless(importlib.util.find_spec('pstats'), "Module pstats not found")
class TimeTestsSqllexPostgres(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.complexity = 1000
        cls.db_name = f"test_sqllex_db"

        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='admin'
        )
        conn.autocommit = True
        cls.admin_cur = conn.cursor()

        try:
            cls.admin_cur.execute("drop database test_sqllex")

        except psycopg2.errors.InvalidCatalogName:
            pass

        try:
            cls.admin_cur.execute("drop user test_sqllex")

        except psycopg2.errors.UndefinedObject:
            pass

        cls.admin_cur.execute("create user test_sqllex with password 'test_sqllex'")
        cls.admin_cur.execute("alter role test_sqllex set client_encoding to 'utf8'")
        cls.admin_cur.execute("alter role test_sqllex set default_transaction_isolation to 'read committed'")
        cls.admin_cur.execute("alter role test_sqllex set timezone to 'UTC'")

        cls.admin_cur.execute("create database test_sqllex owner test_sqllex")

        cls.db = PostgreSQLx(
            engine=psycopg2,
            dbname='test_sqllex',
            user='test_sqllex',
            password='test_sqllex'
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.db.disconnect()
        cls.admin_cur.execute("drop database test_sqllex")
        cls.admin_cur.execute("drop user test_sqllex")

    @save_prof
    def test_create_table(self):
        self.db.create_table(
            'main',
            {
                'id': [SERIAL, PRIMARY_KEY, UNIQUE],
                'name': [TEXT],
                'age': [INTEGER, DEFAULT, 33]
            }
        )

    @save_prof
    def test_insert_fast(self):
        for _ in range(self.complexity):
            self.db.insert('main', (_, f'Alex', 33))

    @save_prof
    def test_insert_slow(self):
        for _ in range(self.complexity, 2*self.complexity):
            self.db.insert('main', (_, 'Alex'))

    @save_prof
    def test_insert_many_fast(self):
        data = [(_, 'Alex', 33) for _ in range(2*self.complexity, 3*self.complexity)]

        self.db.insertmany('main', data)

    @save_prof
    def test_insert_many_slow(self):
        data = [(_, 'Alex') for _ in range(3*self.complexity, 4*self.complexity)]

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

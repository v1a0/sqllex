import os
import sqlite3
import unittest
import importlib.util
from sqllex.constants import *
from sqllex.classes import SQLite3x
from sqllex.debug import debug_mode

# debug_mode(True)


class TestSqllexSQLite(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.tests_counter = 0

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self) -> None:
        self.tests_counter += 1
        self.db_name = f"test_sqllex_db_{self.tests_counter}"

        self.db = SQLite3x(path=self.db_name)

    def tearDown(self) -> None:
        self.db.disconnect()
        os.remove(self.db_name)

    def raw_sql_get_tables_names(self):
        return tuple(map(lambda ret: ret[0], self.db.execute("SELECT name FROM sqlite_master WHERE type='table'")))

    def test_sqlite_db_crating_db(self):
        """
        Testing SQLite database init
        """

        db_name = f"{self.db_name}_{1}"
        SQLite3x(db_name)
        self.assertTrue(os.path.isfile(db_name))
        os.remove(db_name)

        db_name = f"{self.db_name}_{2}"
        SQLite3x(path=db_name)
        self.assertTrue(os.path.isfile(db_name))
        os.remove(db_name)

        db_name = f"{self.db_name}_{3}"
        SQLite3x(db_name, init_connection=False)
        self.assertFalse(os.path.isfile(db_name))

        db_name = f""
        self.assertRaises(ValueError, SQLite3x, db_name)

        db_name = f""
        self.assertRaises(ValueError, SQLite3x, db_name)

        db_name = f""
        self.assertRaises(ValueError, SQLite3x, path=db_name)

    def test_connection(self):
        """
        Testing connection with class object init
        """

        db_name = f"{self.db_name}_{1}"
        self.assertIsInstance(SQLite3x(db_name).connection, sqlite3.Connection)
        os.remove(db_name)

        db_name = f"{self.db_name}_{1}"
        self.assertIsInstance(SQLite3x(db_name, init_connection=True).connection, sqlite3.Connection)
        os.remove(db_name)

        db_name = f"{self.db_name}_{1}"
        self.assertIs(SQLite3x(db_name, init_connection=False).connection, None)

    def test_create_table_1(self):
        """
        Testing table creating
        """

        self.assertRaises(ValueError, self.db.create_table, 'test_table_1', {})
        self.assertRaises(ValueError, self.db.create_table, 'test_table_2', '')

    def test_create_table_basic(self):
        """
        Testing table creating
        """
        columns = {'id': INTEGER}

        self.db.create_table(
            'test_table_1',
            columns
        )
        self.assertEqual(self.raw_sql_get_tables_names(), ('test_table_1',))

        self.db.create_table(
            'test_table_2',
            columns
        )
        self.assertEqual(self.raw_sql_get_tables_names(), ('test_table_1', 'test_table_2'))

    def test_create_table_all_columns(self):
        """
        Testing table creating
        """

        self.db.create_table(
            name='test_table',
            columns={
                'id': [INTEGER, AUTOINCREMENT, PRIMARY_KEY],
                'user': [TEXT, UNIQUE, NOT_NULL],
                'about': [TEXT, DEFAULT, NULL],
                'status': [TEXT, DEFAULT, 'offline']
            }
        )
        self.assertEqual(self.raw_sql_get_tables_names(), ('test_table', 'sqlite_sequence'))

        self.db.create_table(
            name='test_table_1',
            columns={
                'id': [INTEGER, AUTOINCREMENT, PRIMARY_KEY],
                'user': [TEXT, UNIQUE, NOT_NULL],
                'about': [TEXT, DEFAULT, NULL],
                'status': [TEXT, DEFAULT, 'offline']
            }
        )
        self.assertEqual(self.raw_sql_get_tables_names(), ('test_table', 'sqlite_sequence', 'test_table_1'))

    def test_create_table_inx(self):
        """
        Testing if not exist kwarg
        """
        columns = {'id': INTEGER}

        self.db.create_table('test_table_1', columns, IF_NOT_EXIST=True)
        self.db.create_table('test_table_2', columns, IF_NOT_EXIST=True)
        self.db.create_table('test_table_1', columns, IF_NOT_EXIST=True)

        self.assertEqual(self.raw_sql_get_tables_names(), ('test_table_1', 'test_table_2'))
        self.assertRaises(sqlite3.OperationalError, self.db.create_table, 'test_table_1', columns, IF_NOT_EXIST=False)

    def test_markup(self):
        """
        Markup table
        """

        self.db.markup(
            {
                "tt_groups": {
                    "group_id": [PRIMARY_KEY, UNIQUE, INTEGER],
                    "group_name": [TEXT, NOT_NULL, DEFAULT, "GroupName"],
                },

                "tt_users": {
                    "user_id": [INTEGER, PRIMARY_KEY, UNIQUE],
                    "user_name": TEXT,
                    "group_id": INTEGER,

                    FOREIGN_KEY: {
                        "group_id": ["tt_groups", "group_id"]
                    },
                }
            }
        )

        self.assertEqual(
            self.raw_sql_get_tables_names(),
            ('tt_groups', 'tt_users')
        )

    def test_drop_and_create_table(self):
        """
        Create and remove table
        """
        self.db.execute(
            """
            CREATE  TABLE  "test_table"  (
            "id" INTEGER
            );
            """
        )
        self.assertEqual(
            self.raw_sql_get_tables_names(),
            ('test_table',)
        )

        self.db.drop('test_table')
        self.assertEqual(
            self.raw_sql_get_tables_names(),
            tuple()
        )

    def test_insert(self):
        """
        All kind of possible inserts without extra arguments (OR, WITH)
        """

        def get_all_records():
            return self.db.execute(f'SELECT * FROM "{table_name}"')

        def count_all_records():
            return len(get_all_records())

        def count_records(step: int = None):
            """
            This decorator adding counting
            with every run of decorated function it increases count_records.counter at value of step

                @count_records(step=1)
                def func(*args, **kwargs):
                    return None

                func()
                func()

                count_records.counter == 2
            """

            def wrapper_(func: callable):
                def wrapper(*args, **kwargs):
                    # one run == + step records
                    count_records.counter += func.step

                    func(*args, **kwargs)

                    # checking was it inserted or not
                    self.assertEqual(
                        count_all_records(),
                        count_records.counter,
                        msg=f"Incorrect records amount\n args={args}, kwargs={kwargs}"
                    )

                func.step = step

                return wrapper

            if step is None:
                step = 1

            count_records.counter = 0

            return wrapper_

        @count_records(step=2)  # warning - magic number!
        def insert_process(*args, **kwargs):
            self.db.insert(table_name, *args, **kwargs)
            self.db[table_name].insert(*args, **kwargs)

        @count_records(step=10)  # warning - magic number!
        def insert_many_process(*args, **kwargs):
            self.db.insertmany(table_name, *args, **kwargs)
            self.db[table_name].insertmany(*args, **kwargs)

        table_name = 'test_table'
        columns = ("text_c", "num_c", "int_c", "real_c", 'none_c', 'blob_c')
        data = ('asdf', 10.0, 1, 3.14, None, 2)

        self.db.execute(
            """
            CREATE  TABLE IF NOT EXISTS "test_table" (
            "text_c" TEXT,
            "num_c" NUMERIC,
            "int_c" INTEGER,
            "real_c" REAL,
            "none_c" NONE,
            "blob_c" BLOB
            );
            """
        )

        # columns_types = (TEXT, NUMERIC, INTEGER, REAL, NONE, BLOB)
        #
        # self.db.markup(
        #     {
        #         table_name: dict(zip(columns, columns_types))
        #     }
        # )

        # just arg values
        # 1, 2, 3
        insert_process(*data)

        # arg list
        # [1, 2, 3]
        insert_process(list(data))

        # arg tuple
        # (1, 2, 3)
        insert_process(tuple(data))

        # arg tuple
        # {'col1': 1, 'col2': 2}
        insert_process(dict(zip(columns, data)))

        # kwargs
        # col1=1, col2=2
        insert_process(**dict(zip(columns, data)))

        # not full tuple
        insert_process(('asdf', 10.0))

        # not full tuple
        insert_process(['asdf', 10.0])

        # insert_many args
        # (1, 2), (3, 4) ...
        insert_many_process(*((data,) * 5))

        # insert_many one arg
        # ((1, 2), (3, 4) ... )
        insert_many_process((data,) * 5)

        # Manually SQL script execution
        all_data = get_all_records()

        self.assertEqual(all_data, self.db.select(table_name))
        self.assertEqual(all_data, self.db.select(table_name, ALL))
        self.assertEqual(all_data, self.db.select(table_name, '*'))
        self.assertEqual(all_data, self.db[table_name].select_all())
        self.assertEqual(all_data, self.db[table_name].select())
        self.assertEqual(all_data, self.db[table_name].select(ALL))

    def test_insert_xa_and_update(self):
        """
        Insert with extra args and Update
        """

        def re_init_database():
            self.db.executescript(
                """
                DROP TABLE IF EXISTS "salt";
                DROP TABLE IF EXISTS "hashes";
                
                CREATE  TABLE IF NOT EXISTS "hashes" (
                    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "value" TEXT
                );
                
                CREATE  TABLE "salt" (
                    "hashID" INTEGER PRIMARY KEY AUTOINCREMENT,
                    "value" TEXT,
                    
                    FOREIGN KEY (hashID) REFERENCES hashes (id)
                );
                
                INSERT INTO "hashes" (id, value) VALUES (1, '6432642426695757642'), (2, '3259279587463616469'), 
                    (3, '4169263184167314937'), (4, '-8758758971870855856'), (5, '-2558087477551224077');
                
                INSERT INTO "salt" (hashID, value) VALUES (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5');
                """
            )

        # sqlite3.IntegrityError: UNIQUE constraint failed: hashes.id
        re_init_database()
        self.assertRaises(
            sqlite3.IntegrityError,
            self.db.insert, 'hashes', (1, 'newHash'),
        )

        # INSERT OR FAIL
        # sqlite3.IntegrityError: UNIQUE constraint failed: hashes.id
        re_init_database()
        self.assertRaises(
            sqlite3.IntegrityError,
            self.db.insert,
            'hashes', (1, 'newHash'), OR=FAIL
        )

        # INSERT OR ABORT
        # sqlite3.IntegrityError: UNIQUE constraint failed: hashes.id
        re_init_database()
        self.assertRaises(
            sqlite3.IntegrityError,
            self.db.insert,
            'hashes', (1, 'newHash'), OR=ABORT
        )

        # INSERT OR ROLLBACK
        # sqlite3.IntegrityError: UNIQUE constraint failed: hashes.id
        re_init_database()
        self.assertRaises(
            sqlite3.IntegrityError,
            self.db.insert,
            'hashes', (1, 'newHash'), OR=ROLLBACK
        )

        # INSERT OR REPLACE
        re_init_database()
        self.db.insert(
            'hashes',
            (1, 'newHash'),
            OR=REPLACE
        )
        self.assertEqual(
            [
                (1, 'newHash'),
                (2, '3259279587463616469'),
                (3, '4169263184167314937'),
                (4, '-8758758971870855856'),
                (5, '-2558087477551224077')
            ],
            self.db.execute("SELECT * FROM hashes"),
        )

        # INSERT OR IGNORE
        re_init_database()
        self.db.insert(
            'hashes',
            (1, 'newHash'),
            (2, 'anotherNewHash'),
            OR=IGNORE
        )
        self.assertEqual(
            [
                (1, '6432642426695757642'),
                (2, '3259279587463616469'),
                (3, '4169263184167314937'),
                (4, '-8758758971870855856'),
                (5, '-2558087477551224077')
            ],
            self.db.execute("SELECT * FROM hashes"),
        )

        # INSERT many OR REPLACE
        re_init_database()
        self.db.insertmany(
            'hashes',
            (
                (1, 'newHash'),
                (6, 'anotherNewHash'),
            ),
            OR=REPLACE
        )
        self.assertEqual(
            [
                (1, 'newHash'),
                (2, '3259279587463616469'),
                (3, '4169263184167314937'),
                (4, '-8758758971870855856'),
                (5, '-2558087477551224077'),
                (6, 'anotherNewHash'),
            ],
            self.db.execute("SELECT * FROM hashes"),
        )

        # INSERT many OR IGNORE
        re_init_database()
        self.db.insertmany(
            'hashes',
            (
                (1, 'newHash'),
                (6, 'anotherNewHash'),
            ),
            OR=IGNORE
        )
        self.assertEqual(
            [
                (1, '6432642426695757642'),
                (2, '3259279587463616469'),
                (3, '4169263184167314937'),
                (4, '-8758758971870855856'),
                (5, '-2558087477551224077'),
                (6, 'anotherNewHash'),
            ],
            self.db.execute("SELECT * FROM hashes")
        )

        expected = [
            (1, 'newHash'),
            (2, '3259279587463616469'),
            (3, '4169263184167314937'),
            (4, '-8758758971870855856'),
            (5, '-2558087477551224077')
        ]

        # UPDATE
        re_init_database()
        self.db.update(
            'hashes',
            SET={'value': 'newHash'},
            WHERE={'id': 1}
        )
        self.assertEqual(
            expected,
            self.db.execute("SELECT * FROM hashes"),
        )

        # UPDATE
        re_init_database()
        self.db.update(
            'hashes',
            SET={
                self.db['hashes']['value']: 'newHash'
            },
            WHERE={
                self.db['hashes']['id']: 1
            }
        )
        self.assertEqual(
            expected,
            self.db.execute("SELECT * FROM hashes"),
        )

        # UPDATE
        re_init_database()
        self.db.update(
            'hashes',
            SET={
                self.db['hashes']['value']: 'newHash'
            },
            WHERE=self.db['hashes']['id'] == 1
        )
        self.assertEqual(
            expected,
            self.db.execute("SELECT * FROM hashes"),
        )

        # UPDATE
        re_init_database()
        self.db.update(
            'hashes',
            SET={
                self.db['hashes']['value']: 'newHash'
            },
            WHERE=(1 < self.db['hashes']['id']) & (self.db['hashes']['id'] < 5)
        )
        self.assertEqual(
            self.db.execute("SELECT * FROM hashes"),
            [
                (1, '6432642426695757642'),
                (2, 'newHash'),
                (3, 'newHash'),
                (4, 'newHash'),
                (5, '-2558087477551224077')
            ]
        )

        # UPDATE with impossible WHERE condition
        re_init_database()
        self.db.update(
            'hashes',
            SET={
                self.db['hashes']['value']: 'newHash'
            },
            WHERE=(self.db['hashes']['id'] > 9999)
        )
        self.assertEqual(
            self.db.execute("SELECT * FROM hashes"),
            [
                (1, '6432642426695757642'),
                (2, '3259279587463616469'),
                (3, '4169263184167314937'),
                (4, '-8758758971870855856'),
                (5, '-2558087477551224077')
            ]
        )

    def test_select(self):
        """
        All kind of selects (WHERE, ORDER BY, JOIN, GROUP BY)
        """

        self.db.executescript(
            """
            CREATE  TABLE IF NOT EXISTS "position"  (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "name" TEXT,
            "description" TEXT DEFAULT NULL
            );

            CREATE  TABLE IF NOT EXISTS "employee"  (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "firstName" TEXT,
            "surname" TEXT,
            "age" INTEGER NOT NULL,
            "positionID" INTEGER,
            FOREIGN KEY (positionID) REFERENCES position (id)
            );

            CREATE  TABLE IF NOT EXISTS "payments"  (
            "date" TEXT,
            "employeeID" INTEGER,
            "amount" INTEGER NOT NULL
            );
            """
        )

        # self.db.markup(
        #     {
        #         'position': {
        #             'id': [INTEGER, PRIMARY_KEY, AUTOINCREMENT],
        #             'name': TEXT,
        #             'description': [TEXT, DEFAULT, NULL],
        #         },
        #         'employee': {
        #             'id': [INTEGER, PRIMARY_KEY, AUTOINCREMENT],
        #             'firstName': TEXT,
        #             'surname': TEXT,
        #             'age': [INTEGER, NOT_NULL],
        #             'positionID': INTEGER,
        #
        #             FOREIGN_KEY: {
        #                 'positionID': ['position', 'id']
        #             }
        #         },
        #         'payments': {
        #             'date': [TEXT],
        #             'employeeID': INTEGER,
        #             'amount': [INTEGER, NOT_NULL],
        #
        #             FOREIGN_KEY: {
        #                 'positionID': ['employee', 'id']
        #             },
        #         }
        #     }
        # )

        self.db.executemany(
            'INSERT INTO "position" (id, name, description) VALUES (?, ?, ?)',
            (
                (0, 'Assistant', 'Novice developer'),
                (1, 'Junior', 'Junior developer'),
                (2, 'Middle', 'Middle developer'),
                (3, 'Senior', 'senior developer'),
                (4, 'DevOps', 'DevOps engineer')
            )
        )

        self.db.executemany(
            'INSERT INTO "employee" (id, firstName, surname, age, positionID) VALUES (?, ?, ?, ?, ?)',
            (
                (None, 'Alis', 'A', 11, 1),
                (None, 'Bob', 'B', 22, 1),
                (None, 'Carl', 'C', 33, 2),
                (None, 'Alis', 'B', 44, 3),
                (None, 'Dexter', 'B', 55, 1),
                (None, 'Elis', 'A', 22, 1),
                (None, 'Frank', 'B', 33, 1),
                (None, 'Georgy', 'D', 22, 2),
                (None, 'FoxCpp', 'M', 22, 1),
                (None, 'Ira', 'D', 22, 2)
            )
        )

        self.db.executemany(
            'INSERT INTO "payments" (date, employeeID, amount) VALUES (?, ?, ?)',
            (
                ('01.01.2022', 2, 2000),
                ('01.01.2022', 3, 3000),
                ('01.01.2022', 7, 2000),
                ('01.02.2022', 1, 4000),
                ('01.02.2022', 2, 2000),
                ('01.02.2022', 3, 4000),
                ('01.02.2022', 5, 2000),
                ('01.02.2022', 6, 4000),
                ('01.02.2022', 7, 2000),
            )
        )

        # SELECT all
        expected = self.db.execute('SELECT * FROM "employee"')

        self.assertEqual(
            expected, self.db['employee'].select(ALL)
        )
        self.assertEqual(
            expected, self.db['employee'].select_all()
        )
        self.assertEqual(
            expected, self.db['employee'].select_all(GROUP_BY=1)
        )

        # SELECT one column
        expected = self.db.execute('SELECT id FROM "employee"')

        self.assertEqual(
            expected, self.db.select('employee', 'id')
        )
        self.assertEqual(
            expected, self.db['employee']['id']
        )
        self.assertEqual(
            expected, self.db['employee'].select('id')
        )
        self.assertEqual(
            expected, self.db['employee'].select(self.db['employee']['id'])
        )
        self.assertEqual(
            expected, self.db['employee'].select([self.db['employee']['id']])
        )
        self.assertEqual(
            expected, self.db['employee'].select((self.db['employee']['id'],))
        )

        # SELECT 2 columns
        expected = self.db.execute('SELECT id, firstName FROM "employee"')

        self.assertEqual(
            expected, self.db['employee'].select('id, firstName')
        )
        self.assertEqual(
            expected, self.db['employee'].select(['id', 'firstName'])
        )
        self.assertEqual(
            expected, self.db['employee'].select(('id', 'firstName'))
        )
        self.assertEqual(
            expected, self.db['employee'].select(
                [
                    self.db['employee']['id'],
                    self.db['employee']['firstName']
                ]
            )
        )

        # SELECT 2 columns WHERE (condition)
        expected = self.db.execute('SELECT id, firstName FROM "employee" WHERE id > 2')

        self.assertEqual(
            expected,
            self.db['employee'].select(
                SELECT=['id', 'firstName'],
                WHERE='id > 2',
            )
        )
        self.assertEqual(
            expected,
            self.db['employee'].select(
                SELECT=['id', 'firstName'],
                WHERE='id > 2'
            )
        )
        self.assertEqual(
            expected,
            self.db['employee'].select(
                SELECT=['id', 'firstName'],
                WHERE=(self.db['employee']['id'] > 2)
            )
        )
        self.assertEqual(
            expected,
            self.db['employee'].select(
                SELECT=[self.db['employee']['id'], self.db['employee']['firstName']],
                WHERE=(self.db['employee']['id'] > 2)
            )
        )

        # SELECT 2 columns WHERE (condition) AND (condition)
        expected = self.db.execute('SELECT id, firstName FROM "employee" WHERE (age > 11) AND (positionID <> 2)')

        self.assertEqual(
            expected,
            self.db['employee'].select(
                SELECT=['id', 'firstName'],
                WHERE=(self.db['employee']['age'] > 11) & (self.db['employee']['positionID'] != 2)
            )
        )

        # SELECT 2 columns WHERE (condition) AND (condition)
        expected = self.db.execute('SELECT id, firstName FROM "employee" WHERE (age == 11) AND (positionID == 2)')

        self.assertEqual(
            expected,
            self.db['employee'].select(
                SELECT=['id', 'firstName'],
                WHERE=(self.db['employee']['age'] == 11) & (self.db['employee']['positionID'] == 2)
            )
        )

        # SELECT 2 columns WHERE (condition) OR (condition)
        expected = self.db.execute('SELECT id, firstName FROM "employee" WHERE (age == 11) OR (positionID == 2)')

        self.assertEqual(
            expected,
            self.db['employee'].select(
                SELECT=['id', 'firstName'],
                WHERE=(self.db['employee']['age'] == 11) | (self.db['employee']['positionID'] == 2)
            )
        )

        # SELECT 3 columns ORDERED BY column
        expected = self.db.execute('SELECT id, firstName, positionID FROM "employee" ORDER BY positionID')

        self.assertEqual(
            expected,
            self.db['employee'].select(
                SELECT=['id', 'firstName', 'positionID'],
                ORDER_BY='positionID'
            )
        )
        self.assertEqual(
            expected,
            self.db['employee'].select(
                SELECT=['id', 'firstName', 'positionID'],
                ORDER_BY=3
            )
        )
        self.assertEqual(
            expected,
            self.db['employee'].select(
                SELECT=['id', 'firstName', 'positionID'],
                ORDER_BY=['positionID']
            )
        )
        self.assertEqual(
            expected,
            self.db['employee'].select(
                SELECT=['id', 'firstName', 'positionID'],
                ORDER_BY=('positionID',)
            )
        )

        # SELECT 2 columns ORDERED BY column1, column2
        expected = self.db.execute('SELECT id, firstName FROM "employee" ORDER BY firstName, surname')

        self.assertEqual(
            expected,
            self.db['employee'].select(
                SELECT=['id', 'firstName'],
                ORDER_BY=['firstName', 'surname']
            )
        )
        self.assertEqual(
            expected,
            self.db['employee'].select(
                SELECT=['id', 'firstName'],
                ORDER_BY=('firstName', 'surname')
            )
        )

        # SELECT 2 columns ORDERED BY column ASC
        expected = self.db.execute('SELECT id, firstName FROM "employee" ORDER BY firstName ASC')

        self.assertEqual(
            expected,
            self.db['employee'].select(
                SELECT=['id', 'firstName'],
                ORDER_BY='firstName ASC'
            )
        )

        # SELECT 2 columns ORDERED BY column DESC
        expected = self.db.execute('SELECT id, firstName FROM "employee" ORDER BY firstName DESC')

        self.assertEqual(
            expected,
            self.db['employee'].select(
                SELECT=['id', 'firstName'],
                ORDER_BY='firstName DESC'
            )
        )

        # Issue #59 (fixed)
        # self.assertRaises(
        #     sqlite3.OperationalError,
        #     self.db['employee'].select,
        #     SELECT=['id', 'firstName'],
        #     ORDER_BY=['firstName', 'ASC', 'surname', 'DESC']
        # )
        # self.assertRaises(
        #     sqlite3.OperationalError,
        #     self.db['employee'].select,
        #     SELECT=['id', 'firstName'],
        #     ORDER_BY=('firstName', 'ASC', 'surname', 'DESC')
        # )

        # When issue #59 will be fixed, this code have to work fine
        #
        # SELECT 2 columns ORDERED BY column1 ASC, column DESC
        expected = self.db.execute('SELECT id, firstName FROM "employee" ORDER BY firstName ASC, surname DESC')

        self.assertEqual(
            expected,
            self.db['employee'].select(
                SELECT=['id', 'firstName'],
                ORDER_BY=['firstName', 'ASC', 'surname', 'DESC']
            )
        )
        self.assertEqual(
            expected,
            self.db['employee'].select(
                SELECT=['id', 'firstName'],
                ORDER_BY=('firstName', 'ASC', 'surname', 'DESC')
            )
        )

        # SELECT with one INNER JOIN
        expected = self.db.execute(''
                                   'SELECT e.id, e.firstName, p.name '
                                   'FROM employee e '
                                   'INNER JOIN position p '
                                   'ON e.positionID == p.id '
                                   'ORDER BY e.positionID DESC')

        self.assertEqual(
            expected,
            self.db['employee'].select(
                SELECT=[
                    self.db['employee']['id'],
                    self.db['employee']['firstName'],
                    self.db['position']['name']
                ],
                JOIN=(
                    INNER_JOIN, self.db['position'],
                    ON, self.db['position']['id'] == self.db['employee']['positionID']
                ),
                ORDER_BY=(
                    self.db['position']['id'],
                    'DESC'
                )
            )
        )

        # SELECT with two INNER JOINS
        expected = self.db.execute(''
                                   'SELECT e.id, e.firstName, p.name '
                                   'FROM employee e '
                                   'INNER JOIN position p '
                                   'ON e.positionID == p.id '
                                   'INNER JOIN payments '
                                   'ON e.id == payments.employeeID '
                                   'ORDER BY payments.amount DESC')

        self.assertEqual(
            expected,
            self.db['employee'].select(
                SELECT=[
                    self.db['employee']['id'],
                    self.db['employee']['firstName'],
                    self.db['position']['name']
                ],
                JOIN=(
                    (
                        INNER_JOIN, self.db['position'],
                        ON, self.db['position']['id'] == self.db['employee']['positionID']
                    ),
                    (
                        INNER_JOIN, self.db['payments'],
                        ON, self.db['employee']['id'] == self.db['payments']['employeeID']
                    )
                ),
                ORDER_BY=(
                    self.db['payments']['amount'],
                    'DESC'
                )
            )
        )

        # SELECT with two FULL JOINS
        expected = self.db.execute(''
                                   'SELECT e.id, e.firstName, p.name '
                                   'FROM employee e '
                                   'LEFT JOIN position p '
                                   'ON e.positionID == p.id '
                                   'LEFT JOIN payments '
                                   'ON e.id == payments.employeeID '
                                   'ORDER BY payments.amount DESC')

        self.assertEqual(
            expected,
            self.db['employee'].select(
                SELECT=[
                    self.db['employee']['id'],
                    self.db['employee']['firstName'],
                    self.db['position']['name']
                ],
                JOIN=(
                    (
                        LEFT_JOIN, self.db['position'],
                        ON, self.db['position']['id'] == self.db['employee']['positionID']
                    ),
                    (
                        LEFT_JOIN, self.db['payments'],
                        ON, self.db['employee']['id'] == self.db['payments']['employeeID']
                    )
                ),
                ORDER_BY=(
                    self.db['payments']['amount'],
                    'DESC'
                )
            )
        )

        # SELECT * FROM employee GROUP BY
        expected = self.db.execute("SELECT * FROM employee GROUP BY surname")
        self.assertEqual(
            expected,
            self.db.select(SELECT=ALL, FROM='employee', GROUP_BY='surname')
        )
        self.assertEqual(
            expected,
            self.db.select(SELECT=ALL, FROM='employee', GROUP_BY=('surname',))
        )
        self.assertEqual(
            expected,
            self.db.select(SELECT=ALL, FROM='employee', GROUP_BY=['surname'])
        )
        self.assertEqual(
            expected,
            self.db.select(SELECT=ALL, FROM='employee', GROUP_BY=self.db['employee']['surname'])
        )
        self.assertEqual(
            expected,
            self.db.select(SELECT=ALL, FROM='employee', GROUP_BY=(self.db['employee']['surname'],))
        )

        # SELECT * FROM employee GROUP BY 2 rows
        expected = self.db.execute("SELECT * FROM employee GROUP BY surname, positionID")
        self.assertEqual(
            expected,
            self.db.select(SELECT=ALL, FROM='employee', GROUP_BY='surname, positionID')
        )
        self.assertEqual(
            expected,
            self.db.select(SELECT=ALL, FROM='employee', GROUP_BY=('surname', 'positionID'))
        )
        self.assertEqual(
            expected,
            self.db.select(SELECT=ALL, FROM='employee', GROUP_BY=['surname', 'positionID'])
        )

        # SELECT with JOINS GROUP BY
        expected = self.db.execute(''
                                   'SELECT pos.name, pay.amount '
                                   'FROM payments pay '
                                   'INNER JOIN employee emp '
                                   'ON emp.id == pay.employeeID '
                                   'INNER JOIN position pos '
                                   'ON emp.positionID == pos.id '
                                   'GROUP BY pos.name '
                                   'ORDER BY pay.amount DESC')

        self.assertEqual(
            expected,
            self.db['employee'].select(
                SELECT=[
                    self.db['position']['name'],
                    self.db['payments']['amount'],
                ],
                JOIN=(
                    (
                        INNER_JOIN, self.db['payments'],
                        ON, self.db['payments']['employeeID'] == self.db['employee']['id']
                    ),
                    (
                        INNER_JOIN, self.db['position'],
                        ON, self.db['position']['id'] == self.db['employee']['positionID']
                    )
                ),
                GROUP_BY=self.db['position']['name'],
                ORDER_BY=(
                    self.db['payments']['amount'],
                    'DESC'
                )
            )
        )


    def test_extra_features(self):
        """
        Special extra features with no other options to test
        """

        self.db.markup(
            {
                'test_table_1': {
                    'id': INTEGER
                },
                'test_table_2': {
                    'id': INTEGER,
                    'col_1': INTEGER,
                    'col_2': INTEGER,
                    'col_3': INTEGER,
                },
            }
        )

        # Database
        #
        self.assertEqual(self.db.path, self.db_name)

        # Tables
        #
        self.assertEqual(self.raw_sql_get_tables_names(), self.db.tables_names)

        # self.db['notExistingTable']
        self.assertRaises(KeyError, self.db.__getitem__, 'notExistingTable')

        # self.db.get_table('notExistingTable')
        self.assertRaises(KeyError, self.db.get_table, 'notExistingTable')

        self.assertEqual(self.db['test_table_1'].name, 'test_table_1')
        self.assertEqual(self.db['test_table_2'].name, 'test_table_2')

        # Columns
        #
        self.assertEqual(self.db['test_table_1'].columns_names, ('id',))
        self.assertEqual(self.db['test_table_2'].columns_names, ('id', 'col_1', 'col_2', 'col_3'))

        # self.db['notExistingTable']
        self.assertRaises(KeyError, self.db['test_table_1'].__getitem__, 'notExistingColumn')

        self.assertFalse(self.db['test_table_1'].has_column('notExistingColumn'))
        self.assertFalse(self.db['test_table_2'].has_column('notExistingColumn'))

        self.assertEqual(self.db['test_table_1']['id'].name, 'id')
        self.assertEqual(self.db['test_table_2']['id'].name, 'id')

        self.assertEqual(self.db['test_table_1']['id'].table, 'test_table_1')
        self.assertEqual(self.db['test_table_2']['id'].table, 'test_table_2')


    @unittest.skipUnless(importlib.util.find_spec('numpy'), "Module numpy not found")
    def test_numpy(self):
        from numpy import array, nan

        data = [
                ('World', 2415712510, 318.1, '9.7%', nan),
                ('United States', 310645827, 949.5, '44.3%', 'Johnson&Johnson, Moderna, Pfizer/BioNTech'),
                ('India', 252760364, 186.9, '3.5%', 'Covaxin, Covishield, Oxford/AstraZeneca'),
                ('Brazil', 78906225, 376.7, '11.3%', 'Oxford / AstraZeneca, Oxford/AstraZeneca, Pfizer/BioNTech'),
        ]

        self.db.execute(
            """
            CREATE TABLE "test_table_numpy" (
                "Country" TEXT UNIQUE,
                "Doses_Administered" INTEGER,
                "Doses_per_1000" REAL,
                "Fully_Vaccinated_Population" TEXT,
                "Vaccine_Type_Used" TEXT
            );
            """
        )

        self.db.updatemany("test_table_numpy", array(data))
        self.db.updatemany("test_table_numpy", array([[], []]))


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

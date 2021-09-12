# 0.2.0.0

## All you need to know about sqllex 0.2

### Changed returning data type 

```python
db.select(...) -> [(1, 'Data1'), (2, 'Data2')]
```

By now all select-like methods returns `List[Tuple]` instead of `List[List]`

```python
# OLD
db.select(...) -> [[1, 'Data1'], [2, 'Data2']]

# NEW
db.select(...) -> [(1, 'Data1'), (2, 'Data2')]
```

---

### PostgreSQL support
In sqllex v0.2 added basic PostgreSQL support, it's not fully functional now, but it's
in developing progress. It's based on the same structure as SQLite3x and work at the same logic.
If some constants or operator was not added yet, try to enter it as string: 

```python
from sqllex import PostgreSQLx, UNIQUE
from sqllex.constants.postgresql import INT8, SERIAL

db = PostgreSQLx(
    dbname="sqllextests",
    user="postgres",
    password="admin",
    host="127.0.0.1",
    port="5432"
)

# with inline constants
db.create_table(
    name='table1',
    columns={
        'id': SERIAL,
        'value': [INT8, UNIQUE]
    },
    IF_NOT_EXIST=True
)

# w/o inline constants
db.create_table(
    name='table2',
    columns={
        'id': "SERIAL",
        'value': "VARCHAR(32) UNIQUE"
    },
    IF_NOT_EXIST=True
)

print(db.tables_names) # ('table1', 'table2')
```

---

### LIKE support + some syntax sugar

Added LIKE support, and some syntax sugar I called "column-like-regex"
```python
from sqllex import SQLite3x, AbstractTable, AbstractColumn, LIKE

db: SQLite3x = ...
cats: AbstractTable = db['cats']
cats_color: AbstractColumn = cats['color']

dark_cats = cats.select(
    SELECT=('id', 'color'),
    WHERE=(cats_color |LIKE| "%dark%")
)

print(dark_cats)  # [(14, "dark-grey"), (42, "dark-red")]


# another way (issue #39)
dark_cats = cats.select(
    SELECT=('id', 'color'),
    WHERE={
        'color': [LIKE, "%dark%"]
    }
)

print(dark_cats)  # [(14, "dark-grey"), (42, "dark-red")]
```

#### Release candidates chronology

##### v0.2.0.0

- Docs/wiki updates for v0.2.0.0
- Fixed `[LIKE, regex]` for a dict init-ing issue #
- UPDATES.md upd


##### v0.2.0.0-rc5

- Added "column-like-reg_ex" (` WHERE=( column |LIKE| reg_ex ) `)
- Also added LIKE support (issue #39)
- Constants upd (added psql things)
- TableInfoError renamed to TableNotExist
- tuple2list, return2list, lister moved to sqllex.old
- args_parser removed (finally!!!!)
- README upd
- Preparing for release v0.2

##### v0.2.0.0-rc4

- SearchCondition placeholder bugfix
- AbstractTable.replace bugfix
- " ' " -> " " "
- psql.midleware fix
- DEC2FLOAT, float convertion added for psql
- speed-tests remastering

##### v0.2.0.0-rc3

- JoinType renamed to JoinMethod, added JoinArgType
- script_gens got minor update
- postgresqlx.middleware remastering
- postgresqlx placeholder bug fixed
- crop_size remastered (now it's faster)
- functools.wraps removed
- from_as_ remastered (in progress)
- types fix
- JOIN logic changed a little
- content_gen remastered
- args_parser removed from inserting stmts
- other minor fixes. Now it's a little faster and less glitchy

##### v0.2.0.0-rc2

- Placeholders fixed
- Docstrings remastered for SQLite3x and PostgreSQLx
- Pragma methods and generators remover from ABDatabase and moved to sqlite3x dir
- Auto copy docs decorator added
- refactoring args_parser_wrapper
- tests fixed/updated
- preparing psqlx for release

##### v0.2.0.0-rc1

- Added beta PostgreSQL support (new class PostgreSQLx)
- Updated docs-strings for many SQLite3x methods
- Imports optimisation
- Changed border symbol for tables and columns names in scripts from <'> to <"> (due to postgres support)
- New requirement "psycopg2"


---
---
---

# 0.1.10

### 0.1.10.5
- Removed mistaken imports and requirements

### 0.1.10.4
- Insert method got 3x speed up (!!!) using caching
- Select method got 1.68x speed up (!) using caching
- Other methods got <0.1x speed up using caching
- All string generating scripts  moved to core/entities/sqlite3x/script_gens.py
- SQLite3xTable.add_column fixed
- Created custom logger over loguru logger, SqllexLogger
- Typo "ConstrainType" changed to "ConstantType"
- Updated results of speed tests

### 0.1.10.3
- added add_column, remove_column, has_column methods to SQLite3xTable (#22)
- add_column, remove_column to SQLite3x class (#22)
- tests
- SQLite3xColumn and SQLite3xSearchCondition added to sqllex.classes

### 0.1.10.2
- Added 2 new classes SQLiteColumn and SQLite3 SearchCondition with many cool features
- New way to set WHERE  Condition
- New way to set SET Condition
- All select-like methods got changes in args structure (critical!)
- Support column names with spaces
- Bugfix
- Tests upd
- Info files UPDATES and WARNINGS UPD
- fixed issue #15 
- fixed issue #23 
- fixed issue #28 


---
# 0.1.9

### 0.1.9.12
- Fixing #26
- Major restructuring
- code refactoring
- preparing for 0.2
- minor fixes

### 0.1.9.9
- New method UPDATEMANY added for SQLite3x and SQLite3xTable (issue #26)
- INSERTMNAY OR argument issue #26 fixed
- INSERTMNAY empty array shock issue fixed, filter added
- INSERTMNAY minor fixes
- __execute__ decorators got checking stmt valid
- Other minor fixes

### 0.1.9.8
- WITH temporary disabled
- updatemany added
- updatemany removed
- Issue #1 fixed XD

### 0.1.9.5
- Fixed issue #25, now only select-like methods returns data, other methods don't
- Tests update
- SQLStatement and SQLRequest got __bool__ method
- Redame update

### 0.1.9.4
- Bugfix issue #24 "BUG | It should be FROM not TABLE #24"
- UPD Typing for select-like methods

### 0.1.9.3
- Docs remastering
- Removed rudimental code parts
- "wiki" dir removed
- Minor refactoring

### 0.1.9.2
- Issue #18 fixed, exception for sqlite3.OperationalError: no such table: PRAGMA_TABLE_INFO

### 0.1.9.1
- Issue #18 fixed, WHERE argument to update is not required anymore, without WHERE it change all rows in the table


### 0.1.9.0
- Issue #17 fixed, SELECT-like methods now **allways** returns List[List[...]] objects
- Tests remastering
- Code refactoring
- Readme upd

---

# \<=0.1.8

### 0.1.8.12
- Сode refactoring (black code style)
- All methods has been commented
- SQLite3x got __getitem__ method and tables constant
- AS argument removed for all methods
- SQLite3x.tables now (infinite) generator
- SQLite3x got tables_names constant
- SQLite3x.__update_constants__ fixed for multiple db objects
- SQLite3x.JOIN fixed
- args_parser fixed
- SQLite3x.connect method bugfix
- SQLite3x._insertmany_stmt_ bugfix
- SQLite3x._create_stmt_ refactoring bugfix
- SQLite3x._select_stmt_ refactoring bugfix
- SQLite3x.__getitem__ print list of avalible tables_names
- shadow names of wrappers renamed
- Tests added
- __del__ added for SQLite3x
- mistaken warnings removed
- from select_all method remover SELECT var
- For all 'selects' unknown kwargs now getting as WHERE conditions
- Bugfix
- Now Select-like methods always return List object
- Bugfix for get_columns
- insertmany fixed for kwargs of different len
- db.insertmany('wallets', id=[1, 2, 3], balance=[10, ])
- logger got lof_file argument and log2file support
- minor fixes
- Added to methods of SQLite3xTable missing kwargs


### v0.1.7.2 alpha 
- Adeed JOIN support for SELECT method ( __join__ )
- - INNER_JOIN
- - LEFT_JOIN
- - CROSS_JOIN
- - ON
- For FROM arg added "AS" support ( __for_as__ )
- _create_stmt_ fixed
- AUTOINCREMENT issue fixed
- select return tuples or empty lists bug fixed
- logo added


### 0.1.6.5 alpha
- BLOB type added
- Column type issue fixed
- minor bugfix


### 0.1.4 alpha
- WHERE support many args
- Descriptions for methods
- Import fixes
- TODO list upd

### v0.1.3.1 alpha
- Added REPLACE, DELETE methods
- Added parameters WITH, WHERE, OR for most of supported methods
- Pragma method upd
- Major code remastering
- UPDATE method added
- DROP method added
- SELECT return type chaned to List[list]

### v0.1.2 alpha
- Created __insert_stmt__ as parrent method for INSERT ans REPLACE.
- Bugfix for insertmany
- OR comming soon
- Structure upd, preparing for major algho refactoring.
- WITH added for INSERT

### v0.1.1 alpha
- README
- PRAGMA method
- Tests
- Refactoring
- Renaming
- Bug fixes and other minor improvements
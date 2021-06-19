# 0.1.10

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
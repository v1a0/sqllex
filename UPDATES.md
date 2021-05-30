### 0.1.9.1
- Issue #18 fixed, WHERE argument to update is not required anymore, without WHERE it change all rows in the table


### 0.1.9.0
- Issue #17 fixed, SELECT-like methods now **allways** returns List[List[...]] objects
- Tests remastering
- Code refactoring
- Readme upd


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
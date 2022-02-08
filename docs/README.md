 <div style="text-align: center">
<h1> Welcome to the Sqllex Documentation! 👋</h1>
<br>
Here you can find some explanations and examples for Sqllex ORM <br>
</div><br>


## Chapters
- [About](#About)
- [Pages](#Pages)
  - [SQLite3x](about-sqlite3x.md)
  - [SQLite3xTable](about-table.md)
  - [PostgreSQLx](about-postgresqlx.md)
  - [PostgreSQLxTable](about-table.md)
  - [AbstractColumn](about-column.md)
  - [SearchCondition](about-searchcondition.md)
  - [Project Showcase](sqllex-showcase.md)
 
---

# About

### What the heck is Sqllex? 🤔

Sqllex is a python ORM library for comfortable and safe interaction with databases.

If you've ever worked with databases using python, you know what does "Eat nails while writing SQL-scripts" means.
So give a sqllex deal with it, just call needed method, give it a data or necessary parameters and done.

THERE NO `con.cursor()`, only human `db.insert()`, `db.select()`, `db['table']`, 
only beautiful and pythonic code without unnecessary SQL-witchcrafting.

Sqllex has friendly API, documentation and it's awesome for beginners (but not only). 
By the reason it is just an add-on for sqlite3/psycopg2, there will be easy to find explains for typical sqlite3 raised errors.
And also in any moment you can call `db.execute()` method and run any sql-script directly in the database.

It'll be a lot easier to show then explain. So check out examples down below.

---

## Contents

- ### Main classes
- - [Database](./about-sqlite3x.md)
- - [Table](./about-table.md)
- - [Column](./about-column.md)
- - [SearchConditions](./about-searchcondition.md)
- ### Main method
- - [db.select](./database-select.md)
- - [db.insert](./database-insert.md)
- - [db.insertmany](./database-insertmany.md)
- - [db.update](./database-update.md)
- - [db.delete](./database-delete.md)
- - [db.drop](./database-drop.md)
- - [db.markup](./database-markup.md)
- - [db.create_table](./database-create_table.md)
- - [db.add_column](./database-add_column.md)
- - [db.remove_column](./database-remove_column.md)
- - [db.connect](./sqlite3x-connect.md)
- - [db.disconnect](./database-disconnect.md)
- - [db['table_name']](./database-get_table.md)
- ### [Database properties](./database-properties.md)
- ### Examples
- - [Awesome example #0](./examples/sqlite3x-aex-0.md)
- - [Awesome example #1](./examples/sqlite3x-aex-1.md)
  
---

- ### [Project Showcase](sqllex-showcase.md)
  - [Vaccine Update System](sqllex-showcase.md#vaccine-update-systemcase-vsu-src-by-kingabzprokingabzpro)
  - [Sqllex for Data Science Using Pandas](sqllex-showcase.md#sqllex-for-data-science-using-pandascase-dsup-src-by-kingabzprokingabzpro)
  - [Add your own project at this list](https://github.com/v1a0/sqllex/edit/main/docs/sqllex-showcase.md)


---

## How does this work?

Basic idea of sqllex as any ORM is to give user an interface to interact with a database as abstract object.

```markdown
┌───────────────────────────────────────────┐ 
│  DATABASE                                 │        
│     ┌───────────────────────────────────┐ │
│     │  TABLE                            │ │
│     │     ┌───────────────────────────┐ │ │
│     │     │  COLUMN                   │ │ │
│     │     │     ┌───────────────────┐ │ │ │
│     │     │     │  DATA             │ │ │ │
│     │     │     └───────────────────┘ │ │ │
│     │     └───────────────────────────┘ │ │
│     │                                   │ │
│     └───────────────────────────────────┘ │
└───────────────────────────────────────────┘
```

Imagine you have a database called `'server.db'` with only one table inside named `'users'`,
this table has 3 columns `'id'`, `'name'` and `'age'` (so as a pic down below)


```markdown
┌───────────────────────────────────────────┐ 
│  DATABASE 'server.db'                     │             
│     ┌───────────────────────────────────┐ │
│     │  TABLE 'users'                    │ │
│     │     ┌───────────────────────────┐ │ │
│     │     │  COLUMN 'id'              │ │ │
│     │     │     ┌───────────────────┐ │ │ │
│     │     │     │  INTEGER DATA     │ │ │ │
│     │     │     └───────────────────┘ │ │ │
│     │     └───────────────────────────┘ │ │
│     │     ┌───────────────────────────┐ │ │
│     │     │  COLUMN 'name'            │ │ │
│     │     │     ┌───────────────────┐ │ │ │
│     │     │     │  TEXT DATA        │ │ │ │
│     │     │     └───────────────────┘ │ │ │
│     │     └───────────────────────────┘ │ │
│     │     ┌───────────────────────────┐ │ │
│     │     │  COLUMN 'age'             │ │ │
│     │     │     ┌───────────────────┐ │ │ │
│     │     │     │  INTEGER DATA     │ │ │ │
│     │     │     └───────────────────┘ │ │ │
│     │     └───────────────────────────┘ │ │
│     └───────────────────────────────────┘ │
└───────────────────────────────────────────┘
```

With the sqllex you can interact with this database in the craziest way

```python
# Import necessary modules
from sqllex.classes import SQLite3x
from sqllex.constants.sqlite import *

# Database
db = SQLite3x('server.db')

# Create this table
db.create_table(
  'users',
  {
    'id': INTEGER,
    'name': TEXT,
    'age': INTEGER
  },
  IF_NOT_EXIST=True
)

table_users = db['users']
# table_users = db.get_table('users') <-- the same

# add one user
table_users.insert(1, 'Sqllex', 33)

# add 3 more
table_users.insertmany(
  (2, 'Phizilion', 22),
  (3, 'kingabzpro', 44),
  (4, 'asadafasab', 55)
)

print(table_users.select_all()) # [(1, 'Sqllex', 33), (2, 'Phizilion', 22), (3, 'kingabzpro', 44), (4, 'asadafasab', 55)]

# Get column age as object
column_age = table_users['age']

print(
  table_users.select(
    WHERE=(column_age > 40)
  )
) # [(3, 'kingabzpro', 44), (4, 'asadafasab', 55)]


column_name = table_users['name']


print(
  table_users.select(
    WHERE=(column_age > 40) & (column_name |LIKE| 'kin%')
  )
) # [(3, 'kingabzpro', 44)]
```

### Also, you can do crazy things like this

```python
self.db['employee'].select(
    SELECT=[
        db['employee']['id'],
        db['employee']['firstName'],
        db['position']['name']
    ],
    JOIN=(
        (
            LEFT_JOIN, db['position'],
            ON, db['position']['id'] == db['employee']['positionID']
        ),
        (
            INNER_JOIN, self.db['payments'],
            ON, db['employee']['id'] == db['payments']['employeeID']
        )
    ),
    ORDER_BY=(
        db['payments']['amount'],
        'DESC'
    )
)
```


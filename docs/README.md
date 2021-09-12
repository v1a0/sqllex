<div style="text-align: center">
<h1> Welcome to the Sqllex Documentation! 👋</h1>
<br>
Here you can find some explanations and examples for Sqllex ORM <br>
</div><br>


## Chapters
- [About](#About)
- [Pages](#Pages)
  - [SQLite3x](#SQLite3x)
  - [SQLite3xTable](#SQLite3xTable)
  - [SQLite3xColumn](#SQLite3xColumn)
  - [SQLite3xSearchCondition](#SQLite3xSearchCondition)
  - [Common Parameters](#Common-Parameters)
  - [Project Showcase](#Project-Showcase)

---

# About

### What the heck is Sqllex? 🤔

Sqllex is a python ORM library for comfortable and safe interaction with databases.

If you've ever worked with databases using python, you know what does "Eat nails while writing SQL-scripts" means.
So give a sqllex deal with it, just call needed method, give it a data or necessary parameters and it's done.
There no `con.cursor()`, only human `db.insert()`, `db.select()`, `db['my_table']`, only beautiful and pythonic code without unnecessary SQL-witchcrafting.

Sqllex is not like other ORM's, has unfriendly API and awesome for beginners (and not only). 
By the reason it is just an add-on for sqlite3, there will be easy to find explains for typical sqlite3 raised errors.
And any moment you could call `db.execute()` method and run any sql-script directly in sqlite3.

It'll be a lot easier to show then explain. So down below is a few examples.

### If you never used SQLite before read [this awesome example #0](sqlite3x-aex-0.md)  

### Otherwise, you can check out [this one example #1](sqlite3x-aex-1.md)

### [Project showcase](sqllex-showcase.md)

# Pages

- ## SQLite3x
  
  - ### [About class](about-sqlite3x.md) 
    
  - ### Examples
    - [Awesome example #0](sqlite3x-aex-0.md)
    - [Awesome example #1](sqlite3x-aex-1.md)
    
  - ### Methods
    - [insert](database-insert.md)
    - [insertmany](database-insertmany.md)
    - [update](database-update.md)
    - [updatemany](database-updatemany.md)
    - [replace](sqlite3x-replace.md)
    - [select](database-select.md)
    - ~~select_distinct~~
    - [select_all](database-select_all.md)
    - [markup](database-markup.md)
    - [create_table](database-create_table.md)
    - ~~create_temp_table~~
    - ~~create_temporary_table~~
    - [connect](sqlite3x-connect.md)
    - [disconnect](database-disconnect.md)
    - [delete](database-delete.md)
    - [drop](database-drop.md)
    - [get_table](database-get_table.md)
    - [get_columns](database-get_columns.md)
    - [get_columns_names](database-get_columns_names.md)
    - [add_column](database-add_column.md)
    - [remove_column](database-remove_column.md)
    - [pragma, foreign_keys, journal_mode, table_info](sqlite3x-pragma.md)
    - [execute](database-execute.md)
    - [executemany](database-executemany.md)
    - [executescript](database-executescript.md)
    
  - ### [Properties / Constants](sqlite3x-properties.md)
    - [path](sqlite3x-properties.md)
    - [connection](sqlite3x-properties.md)
    - [tables](sqlite3x-properties.md)
    - [tables_names](sqlite3x-properties.md)
  
- ## SQLite3xTable
  
  - ### [About class](about-table.md) 

  - ### Methods
    - [insert](database-insert.md)
    - [insertmany](database-insertmany.md)
    - [update](database-update.md)
    - [updatemany](database-updatemany.md)
    - [replace](sqlite3x-replace.md)
    - [select](database-select.md)
    - ~~select_distinct~~
    - [select_all](database-select_all.md)
    - [delete](database-delete.md)
    - [drop](database-drop.md)
    - [get_columns](database-get_columns.md)
    - [get_columns_names](database-get_columns_names.md)
    - [add_column](database-add_column.md)
    - [remove_column](database-remove_column.md)
    - [has_column](table-has_column.md)
    
  - ### [Properties / Constants](table-properties.md)
    - [db](table-properties.md#sqlite3xtabledb)
    - [name](table-properties.md#sqlite3xtablename)
    - [columns](table-properties.md#sqlite3xtablecolumns)
    - [columns_names](table-properties.md#sqlite3xtablecolumns_names)

- ## SQLite3xColumn
  - ### [About class](about-column.md)
  
- ## SQLite3xSearchCondition
  - ### [About class](searchcondition-about.md)
  
- ## [Common Parameters](all-parameters.md)
  - [SELECT](all-parameters.md#select)
  - [WHERE](all-parameters.md#where)
  - [SET](all-parameters.md#set)
  - [OR](all-parameters.md#or)
  - [~~WITH~~](all-parameters.md#with)
  - [ORDER_BY](all-parameters.md#order_by)
  - [LIMIT](all-parameters.md#limit)
  - [OFFSET](all-parameters.md#offset)
  - [FROM](all-parameters.md#from)
  - [JOIN](all-parameters.md#join)

- ## [Project Showcase](sqllex-showcase.md)
  - [Vaccine Update System](sqllex-showcase.md#vaccine-update-systemhttpsdeepnotecomabidvaccine-update-dashboard-gybicp-ftaydgmjimofj0w--by-kingabzpro)
  - [Sqllex for Data Science Using Pandas](sqllex-showcase.md#sqllex-for-data-science-using-pandashttpsdeepnotecomabidsqllex-simple-and-faster-7wxrco0hrxaqvaixo8qjbq-by-kingabpro)
  - [Add your own project at this list](https://github.com/v1a0/sqllex/edit/main/docs/sqllex-showcase.md)

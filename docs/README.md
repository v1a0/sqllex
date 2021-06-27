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

### If you never used SQLite before read [this awesome example #0](./sqlite3x-aex-0.md)  

### Otherwise, you can check out [this one example #1](./sqlite3x-aex-1.md)

### [Project showcase](sqllex-showcase.md)

# Pages

- ## SQLite3x
  
  - ### [About class](./sqlite3x-about.md) 
    
  - ### Examples
    - [Awesome example #0](./sqlite3x-aex-0.md)
    - [Awesome example #1](./sqlite3x-aex-1.md)
    
  - ### Methods
    - [insert](./sqlite3x-insert.md)
    - [insertmany](./sqlite3x-insertmany.md)
    - [update](./sqlite3x-update.md)
    - [updatemany](./sqlite3x-updatemany.md)
    - [replace](./sqlite3x-replace.md)
    - [select](./sqlite3x-select.md)
    - ~~select_distinct~~
    - [select_all](./sqlite3x-select_all.md)
    - [markup](./sqlite3x-markup.md)
    - [create_table](./sqlite3x-create_table.md)
    - ~~create_temp_table~~
    - ~~create_temporary_table~~
    - [connect](./sqlite3x-connect.md)
    - [disconnect](./sqlite3x-disconnect.md)
    - [delete](./sqlite3x-delete.md)
    - [drop](./sqlite3x-drop.md)
    - [get_table](./sqlite3x-get_table.md)
    - [get_columns](./sqlite3x-get_columns.md)
    - [get_columns_names](./sqlite3x-get_columns_names.md)
    - [add_column](./sqlite3x-add_column.md)
    - [remove_column](./sqlite3x-remove_column.md)
    - [pragma, foreign_keys, journal_mode, table_info](./sqlite3x-pragma.md)
    - [execute](./sqlite3x-execute.md)
    - [executemany](./sqlite3x-executemany.md)
    - [executescript](./sqlite3x-executescript.md)
    
  - ### [Properties / Constants](./sqlite3x-properties.md)
    - [path](./sqlite3x-properties.md)
    - [connection](./sqlite3x-properties.md)
    - [tables](./sqlite3x-properties.md)
    - [tables_names](./sqlite3x-properties.md)
  
- ## SQLite3xTable
  
  - ### [About class](./sqlite3xtable-about.md) 

  - ### Methods
    - [insert](./sqlite3x-insert.md)
    - [insertmany](./sqlite3x-insertmany.md)
    - [update](./sqlite3x-update.md)
    - [updatemany](./sqlite3x-updatemany.md)
    - [replace](./sqlite3x-replace.md)
    - [select](./sqlite3x-select.md)
    - ~~select_distinct~~
    - [select_all](./sqlite3x-select_all.md)
    - [delete](./sqlite3x-delete.md)
    - [drop](./sqlite3x-drop.md)
    - [get_columns](./sqlite3x-get_columns.md)
    - [get_columns_names](./sqlite3x-get_columns_names.md)
    - [add_column](./sqlite3x-add_column.md)
    - [remove_column](./sqlite3x-remove_column.md)
    - [has_column](./sqlite3xtable-has_column.md)
    
  - ### [Properties / Constants](./sqlite3xtable-properties.md)
    - [db](./sqlite3xtable-properties.md#sqlite3xtabledb)
    - [name](./sqlite3xtable-properties.md#sqlite3xtablename)
    - [columns](./sqlite3xtable-properties.md#sqlite3xtablecolumns)
    - [columns_names](./sqlite3xtable-properties.md#sqlite3xtablecolumns_names)

- ## SQLite3xColumn
  - ### [About class](./sqlite3xcolumn-about.md)
  
- ## SQLite3xSearchCondition
  - ### [About class](./sqlite3xsearchcondition-about.md)
  
- ## [Common Parameters](./common-parameters.md)
  - [SELECT](./common-parameters.md#select)
  - [WHERE](./common-parameters.md#where)
  - [SET](./common-parameters.md#set)
  - [OR](./common-parameters.md#or)
  - [~~WITH~~](./common-parameters.md#with)
  - [ORDER_BY](./common-parameters.md#order_by)
  - [LIMIT](./common-parameters.md#limit)
  - [OFFSET](./common-parameters.md#offset)
  - [FROM](./common-parameters.md#from)
  - [JOIN](./common-parameters.md#join)

- ## [Project Showcase](sqllex-showcase.md)
  - [Vaccine Update System](./sqllex-showcase.md#vaccine-update-systemhttpsdeepnotecomabidvaccine-update-dashboard-gybicp-ftaydgmjimofj0w--by-kingabzpro)
  - [Sqllex for Data Science Using Pandas](./sqllex-showcase.md#sqllex-for-data-science-using-pandashttpsdeepnotecomabidsqllex-simple-and-faster-7wxrco0hrxaqvaixo8qjbq-by-kingabpro)
  - [Add your own project at this list](https://github.com/v1a0/sqllex/edit/main/docs/sqllex-showcase.md)

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
  - [SearchCondition](searchcondition-about.md)
  - [Project Showcase](sqllex-showcase.md)
 
---

# About

### What the heck is Sqllex? 🤔

Sqllex is a python ORM library for comfortable and safe interaction with databases.

If you've ever worked with databases using python, you know what does "Eat nails while writing SQL-scripts" means.
So give a sqllex deal with it, just call needed method, give it a data or necessary parameters and it's done.
There no `con.cursor()`, only human `db.insert()`, `db.select()`, `db['my_table']`, 
only beautiful and pythonic code without unnecessary SQL-witchcrafting.

Sqllex is not like other ORM's, has unfriendly API and awesome for beginners (and not only). 
By the reason it is just an add-on for sqlite3, there will be easy to find explains for typical sqlite3 raised errors.
And any moment you could call `db.execute()` method and run any sql-script directly in sqlite3.

It'll be a lot easier to show then explain. So down below is a few examples.

### If you never used SQLite before read [this awesome example #0](sqlite3x-aex-0.md)  

### Otherwise, you can check out [this one example #1](sqlite3x-aex-1.md)

### [Project showcase](sqllex-showcase.md)

# Pages

- ### [SQLite3x](about-sqlite3x.md)
  - [SQLite3xTable](about-table.md) 
  - Examples
    - [Awesome example #0](sqlite3x-aex-0.md)
    - [Awesome example #1](sqlite3x-aex-1.md)
  
- ### [PostgreSQLx](about-postgresqlx.md)
  - [PostgreSQLxTable](about-table.md)
  
- ### [AbstractColumn](about-column.md)
  
- ### [SearchCondition](searchcondition-about.md)
  
- ### [Project Showcase](sqllex-showcase.md)
  - [Vaccine Update System](sqllex-showcase.md#vaccine-update-systemhttpsdeepnotecomabidvaccine-update-dashboard-gybicp-ftaydgmjimofj0w--by-kingabzpro)
  - [Sqllex for Data Science Using Pandas](sqllex-showcase.md#sqllex-for-data-science-using-pandashttpsdeepnotecomabidsqllex-simple-and-faster-7wxrco0hrxaqvaixo8qjbq-by-kingabpro)
  - [Add your own project at this list](https://github.com/v1a0/sqllex/edit/main/docs/sqllex-showcase.md)

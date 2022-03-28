
<div align="center">

<img src="./pics/sqllex-logo.svg" width="300px" alt="sqllex logo">

# SQLLEX ORM v0.2.3

![python-auto-ver]
[![lgtm-quality-img]][lgtm-quality-src]
[![lgtm-alerts-img]][lgtm-alerts-src]

[![pypi-version-img]][pypi-version-src]
[![pypi-downloads-img]][pypi-stats]

[![wiki-img]][wiki-src] [![docs-dark-img]][docs-github]
[![telegram-group-img]][telegram-group-src]


<br>
The most pythonic ORM. Seriously, try it out!<br>
</div><br>


## Installation
```shell
pip install sqllex
```

|   Version    |                              Status                              |                                                  Tests, and actions                                                   |
|:------------:|:----------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------------:|
|  `==0.2.3`   |               ✔️ supported         <br> ✔️ stable                | [![code-ql-img]][code-ql-src] <br> [![sqllex-tests-img]][sqllex-tests-src] <br> [![pypi-upload-img]][pypi-upload-img] |
| `<=0.2.0.4`  | ⚠️ outdated         <br>   ⚠️ Security issue <br>  CVE-2022-0329 |                                                   ⚠️ Mostly passing                                                   |
| `<=0.1.10.4` |                           ❌️ outdated                            |                                                           ❌                                                           |


| Databases  | Support |
| :---       | :-----: |
| SQLite     | ✔️|
| PostgreSQL | ✔️*|

<small>* - partially support</small>

## About
Use databases without thinking about SQL.

Interact with a database as python object by intuitive methods
just like `.insert()`, `.select()` or `.find()`.

Let me show you how sqllex ORM makes your life easier.
Imagine you need create some database, save some data into this
and take it back. That's how your easy to code it with sqllex.


### SQLite3
```python
from sqllex import *

db = SQLite3x(                              
    path='my_database.db',                      
    template={                              
        "users": {                          
            "username": [TEXT, NOT_NULL],   
            "age": INTEGER,                 
        }                                   
    }                                       
)

users = db["users"]

users.insert('Sqllex', 33)

users_33 = users.find(age=33)

print(users_33)  # [('Sqllex', 33)]
```

<br>
<details>
<summary id="what1">WHAT IS GOING ON THERE?!</summary>


```python
from sqllex import *

# Create some database, with simple structure
db = SQLite3x(                              # create database
    path='my_data.db',                      # path to your database, or where you would like it locate
    template={                              # schema for tables inside your database                              
        "users": {                              # name for the 1'st table
            "username": [TEXT, NOT_NULL],       # 1'st column of table, named "username", contains text-data, can't be NULL
            "age": INTEGER,                     # 2'nd column of table, named "age", contains integer value
        }                                   # end of table
    }                                       # end of schema (template)
)

# Ok, now you have database with table inside it.
# Let's take this table as variable
users = db["users"]

# Now add record of 33 years old user named 'Sqllex' into it
# Dear table, please insert ['Sqllex', 33] values
users.insert('Sqllex', 33)

# Dear table, please find records where_ column 'age' == 33
users_33 = users.find(age=33)

# Print results
print(users_33)  # [('Sqllex', 33)]
```

</details>






# Examples
|  DMS | Example |
| :----: | :---:|
| [SQLite3](#sqlite3) | ["Zero level"][awesome-example-0] (v0.2+) |
| [SQLite3](#sqlite3) | ["Pre-Intermediate"][awesome-example-1] (v0.2+) |
| [SQLite3](#sqlite3) | [Data Science][data-science-example] (v0.1.8.4) |
| [SQLite3](#sqlite3) | [Project Showcase][project-showcase] |
| PostgreSQL | - |


# Community

[![stars-image](https://raw.githubusercontent.com/v1a0/metrtics/main/pics/sqllex/stars.svg)](https://github.com/v1a0/sqllex/stargazers)

## Not enough? Read more in [Sqllex Documentation!][wiki-src]

## [Wiki contents][contents]


-----
# Other
#### [UPDATES](./UPDATES.md)
#### [WARNING](./WARNING.md)
#### [LICENSE](./LICENSE)
#### [DOCUMENTATION][wiki-src]




<!-- ALIASES -->

  <!-- Images -->
  [wiki-img]: https://img.shields.io/badge/docs-Wiki-blue.svg
  [docs-dark-img]: https://img.shields.io/badge/dosc-dark%20theme-black
  [python-auto-ver]: https://img.shields.io/pypi/pyversions/sqllex?color=green
  [python-3-10]: https://img.shields.io/badge/Python-3.10-green
  [python-3-9]: https://img.shields.io/badge/Python-3.9-green
  [python-3-8]: https://img.shields.io/badge/Python-3.8-green
  [lgtm-quality-img]: https://img.shields.io/lgtm/grade/python/g/V1A0/sqllex.svg?logo=lgtm&logoWidth=18
  [lgtm-alerts-img]: https://img.shields.io/lgtm/alerts/g/V1A0/sqllex.svg?logo=lgtm&logoWidth=18
  [pypi-version-img]: https://img.shields.io/pypi/v/sqllex.svg
  [pypi-downloads-img]: https://img.shields.io/pypi/dm/sqllex
  [telegram-group-img]: https://img.shields.io/badge/Telegram-Group-blue.svg?logo=telegram
  [code-ql-img]: https://github.com/v1a0/sqllex/actions/workflows/codeql-analysis.yml/badge.svg?branch=main
  [sqllex-tests-img]: https://github.com/v1a0/sqllex/actions/workflows/test_sqllex.yml/badge.svg?branch=main
  [pypi-upload-img]: https://github.com/v1a0/sqllex/actions/workflows/python-publish.yml/badge.svg

  <!-- Sources -->
  [wiki-src]: https://v1a0.github.io/sqllex
  [docs-github]: https://github.com/v1a0/sqllex/tree/main/docs#-welcome-to-the-sqllex-documentation-
  [lgtm-quality-src]: https://lgtm.com/projects/g/V1A0/sqllex/context:python
  [lgtm-alerts-src]: https://lgtm.com/projects/g/V1A0/sqllex/alerts/
  [pypi-version-src]: https://pypi.org/project/sqllex/
  [telegram-group-src]: https://t.me/joinchat/CKq9Mss1UlNlMDIy
  [code-ql-src]: https://github.com/v1a0/sqllex/actions/workflows/codeql-analysis.yml
  [sqllex-tests-src]: https://github.com/v1a0/sqllex/actions/workflows/test_sqllex.yml
  [pypi-upload-src]: https://github.com/v1a0/sqllex/actions/workflows/python-publish.yml
  [awesome-example-0]: https://v1a0.github.io/sqllex/examples/sqlite3x-aex-0.html
  [awesome-example-1]: https://v1a0.github.io/sqllex/examples/sqlite3x-aex-1.html
  [data-science-example]: https://deepnote.com/@abid/SQLLEX-Simple-and-Faster-7WXrco0hRXaqvAiXo8QJBQ
  [project-showcase]: https://v1a0.github.io/sqllex/sqllex-showcase.html
  [pypi-stats]: https://pypistats.org/packages/sqllex
  [contents]: https://v1a0.dev/sqllex/#contents

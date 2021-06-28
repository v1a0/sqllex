
<div align="center">

<img src="./pics/sqllex-logo.svg" width="300px" alt="sqllex logo">

# SQLLEX v0.1.10 📚

![python-3-9]
[![lgtm-quality-img]][lgtm-quality-src]
[![lgtm-alerts-img]][lgtm-alerts-src]

[![pypi-version-img]][pypi-version-src]
[![pypi-downloads-img]][pypi-version-src]

[![Wiki][wiki-img]][wiki-src] 
[![telegram-group-img]][telegram-group-src]


<br>
Better than <b>sqlite3</b>. Seriously, try it out<br>
</div><br>

## Installation
```shell
pip install sqllex
```

If you need most stable version install **sqllex==0.1.10.3**


| Version |  Status | Tests, and actions |
| :--------: | :----------------------------: | :---: |
| `0.1.10.4`    | ✔️ stable (testing)  <br> ✔️ supported      | [![code-ql-img]][code-ql-src] <br> [![sqlite3x-test-img]][sqlite3x-test-src] <br> [![pypi-upload-img]][pypi-upload-img] |
| `0.1.10.3`    | ✔️ stable            <br> ✔️ supported      | ✔️All passed |
| `<=0.1.9.10`  | ✔️ stable            <br> ❌️ outdated       |  ✔️Mostly passing |
| `<= 0.1.8.x`  | ⚠️ unstable          <br> ❌️ outdated       |  ~ |


## About
Use databases without thinking about SQL. Let me show you how sqllex ORM makes
your life easier. Imagine you need create some database, save some data
into it and take it back. That's how your easy to code with sqllex.


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

print(users_33)  # [['Sqllex', 33]]
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
        "users": {                          # name for the 1'st table
            "username": [TEXT, NOT_NULL],   # 1'st column of table, named "username", contains text-data, can't be NULL
            "age": INTEGER,                 # 2'nd column of table, named "age", contains integer value
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
print(users_33)  # [['Sqllex', 33]]
```


</details>

####  If you never used SQLite before read [this awesome example #0][awesome-example-0] instead


# Examples

 - [Awesome example #0][awesome-example-0]
 - [Awesome example #1][awesome-example-1]
 - [Sqllex for Data Science][data-science-example]
 - [Project Showcase][project-showcase] ⭐


# Not enough? Read more in [Sqllex Documentation!][wiki-src]

-----
### Other
#### [UPDATES](./UPDATES.md)
#### [WARNING](./WARNING.md)
#### [LICENSE](./LICENSE)
#### [DOCUMENTATION][wiki-src]


  [wiki-img]: https://img.shields.io/badge/docs-Wiki-blue.svg
  [wiki-src]: https://v1a0.github.io/sqllex

  [python-3-9]: https://img.shields.io/badge/Python-3.9-green

  [python-3-8]: https://img.shields.io/badge/Python-3.8-green

  [lgtm-quality-img]: https://img.shields.io/lgtm/grade/python/g/V1A0/sqllex.svg?logo=lgtm&logoWidth=18
  [lgtm-quality-src]: https://lgtm.com/projects/g/V1A0/sqllex/context:python

  [lgtm-alerts-img]: https://img.shields.io/lgtm/alerts/g/V1A0/sqllex.svg?logo=lgtm&logoWidth=18
  [lgtm-alerts-src]: https://lgtm.com/projects/g/V1A0/sqllex/alerts/
  
  [pypi-version-img]: https://img.shields.io/pypi/v/sqllex.svg
  [pypi-version-src]: https://pypi.org/project/sqllex/
  
  [pypi-downloads-img]: https://img.shields.io/pypi/dm/sqllex
  
  [telegram-group-img]: https://img.shields.io/badge/Telegram-Group-blue.svg?logo=telegram
  [telegram-group-src]: https://t.me/joinchat/CKq9Mss1UlNlMDIy
  
  [code-ql-img]: https://github.com/v1a0/sqllex/actions/workflows/codeql-analysis.yml/badge.svg?branch=main
  [code-ql-src]: https://github.com/v1a0/sqllex/actions/workflows/codeql-analysis.yml
  
  [sqlite3x-test-img]: https://github.com/v1a0/sqllex/actions/workflows/test_sqlite3x.yml/badge.svg?branch=main
  [sqlite3x-test-src]: https://github.com/v1a0/sqllex/actions/workflows/test_sqlite3x.yml
  
  [pypi-upload-img]: https://github.com/v1a0/sqllex/actions/workflows/python-publish.yml/badge.svg
  [pypi-upload-src]: https://github.com/v1a0/sqllex/actions/workflows/python-publish.yml

  [awesome-example-0]: https://v1a0.github.io/sqllex/sqlite3x-aex-0.html
  [awesome-example-1]: https://v1a0.github.io/sqllex/sqlite3x-aex-1.html
  [data-science-example]: https://deepnote.com/@abid/SQLLEX-Simple-and-Faster-7WXrco0hRXaqvAiXo8QJBQ
  [project-showcase]: https://v1a0.github.io/sqllex/sqllex-showcase

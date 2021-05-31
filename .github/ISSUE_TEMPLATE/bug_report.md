---
name: Bug report
about: If you found the bug or something just doesn't seems to work right
title: 'BUG | '
labels: bug
assignees: ''

---

## DESCRIBE THE BUG
A clear description of what the bug is and what might be the reason of it.
Show logs or error message you got.

Example log:
```
File "main.py", line 1337, in <module>
    some= db["some"]
  File "/usr/local/lib/python3.9/site-packages/sqllex/classes/sqlite3x.py", line 999, in __getitem__
    return SQLite3xTable(db=self, name=key)
...
sqlite3.OperationalError: no such table: PRAGMA_TABLE_INFO
```


## CODE
Show the code (or just a few lines) raise this bug. Show what methods you call and what the input data is. MAKE SURE IT DOESN'T CONTAINS ANY PRIVATE DATA! 

For example:
```python
a = 1
b = "Hello world"
table.insert(a, b)
```


## SCREENSHOTS
If applicable, add screenshots to help explain your problem.


## CONFIGURATIONS
 - OS: [Windows10, Ubuntu 20.04, ...]
 - Python version: [3.8, 3.9, 3.9.5, ...]
 - Sqllex version: [0.1.8.12, 0.1.9, 0.1.9.2]

## OTHER

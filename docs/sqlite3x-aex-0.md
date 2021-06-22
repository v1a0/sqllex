# SQLite3x | Awesome example #0

This is basic example, for whom never before used sqlite3x

### First you need to install sqllex by pip

```
pip install sqllex
```


### Create main.py file and 

<img src="https://raw.githubusercontent.com/v1a0/imgs/main/sqllex/examples/1/py_main.png">

<br><br>

### And type some code into it

```python
from sqllex import *

db = SQLite3x()
```

After you run this code you'll see a database file in the same directory as your `mail.py` file

<img src="https://raw.githubusercontent.com/v1a0/imgs/main/sqllex/examples/1/db_and_main.png">

You can open it (by [sqlitebrowser](https://github.com/sqlitebrowser/sqlitebrowser) for example) and make sure it works and it's empty

<img src="https://raw.githubusercontent.com/v1a0/imgs/main/sqllex/examples/1/db_0.png">


<br><br>


### Let's add table into this database
Imagine you need save some data about users consist of `id` and `username`. 

Let's ask db to "`create table` `named` `'users'` with `columns`:
- `'id'` (have to be `integer`)
- `'username'` (have to be `text`-like and can not be empty)". Now type it as code.

```python
db.create_table(
    name='users',
    columns={
        'id': INTEGER,
        'username': [TEXT, NOT_NULL]
    },
    IF_NOT_EXIST=True
)
```

`IF_NOT_EXIST=True` - highly recommend set this argument `True` it'll avoid you an error (in the next runs) if table already exist.

Run it. Done, and results:

<img src="https://github.com/v1a0/imgs/blob/main/sqllex/examples/1/db_1.png">
<img src="https://github.com/v1a0/imgs/blob/main/sqllex/examples/1/db_2.png">


<br><br>


### Awesome table created, it's time to insert some data into it

Take table called `users` (as table_users) and `insert` into this TABLE next data (record): `user_id` in column `id` and `user_name` in column `username` 

```python
user_id = 1
user_name = 'Alex'

table_users = db['users']

table_users.insert(
    id=user_id, username=user_name
)
```

Run it.

<img src="https://github.com/v1a0/imgs/blob/main/sqllex/examples/1/db_3.png">


And yup, we're in! So now we'll take it back.


<br><br>


### Select all records from table

So `select` ALL (by default) form TABLE named `'users'`, save it into var `users` and print it.

```python
users = table_users.select_all()

print(users)    # [1, 'Alex']
```

Run it. It returns:

```python
[1, 'Alex']
```
Great! Now let's add more users.


<br><br>


### Insert many data

It's kind of the same as just `insert` one record, but only use `insertmany` method if you want make it for lists (or tuples) of data. In this example we have 2 lists: 1'st one is lists of ids and 2'nd of usernames. Time to save it

```python
users_ids = [2, 3, 4, 5]
users_names = ['User2', 'User3', 'User4', 'User5']

table_users.insertmany(
    id=users_ids, username=users_names
)
```

<img src="https://github.com/v1a0/imgs/blob/main/sqllex/examples/1/db_4.png">

And select all data from table again:

```python
users = table_users.select_all()

print(users)
```

Returns: 
```python
[[1, 'Alex'], [2, 'User2'], [3, 'User3'], [4, 'User4'], [5, 'User5']]
```

Perfect!


<br><br>


### Little bit more about selects

You have to know that `select` method can be more selective (:D).
You don't have to select all records from table all the time, you can just add a selection condition like `WHERE`

Lets select all records from table `'users'` records satisfying the condition `id == 2`:

```python
user2 = table_users.select(
    WHERE=['id', 2]
)

print(user2)
```

returns:
```python
[2, 'User2']
```

Well done. How about get records `WHERE` `id == 2`:

```python
users_345 = table_users.select(
    WHERE=['id', '>', 2]
)

print(users_345)
```

We got:

```python
[[3, 'User3'], [4, 'User4'], [5, 'User5']]
```

If you need get only `usernames` of records satisfying the condition, set `SELECT` value.

```python
users_names = table_users.select(
    SELECT='username',
    WHERE=['id', '>', 2]
)

print(users_names)
```

We got:

```python
['User3', 'User4', 'User5']
```

Good job!


<br><br>


### Mark up one more table and insert data into it

Earlier we got many lists of records, one of this `users_345`

```python
print(users_345)
```

```python
[[3, 'User3'], [4, 'User4'], [5, 'User5']]
```

Now create one more table but by `mark up` method. And insert users_345 into it

```python
new_table_scheme = {
    'some_users': {
        'id': INTEGER,
        'username': [TEXT, NOT_NULL]
    }
}

db.markup(new_table)

new_table = db['new_table']

new_table.insertmany(users_345)

print(db.tables_str)
```

returns:

```python
['users', 'some_users']
```

<img src="https://github.com/v1a0/imgs/blob/main/sqllex/examples/1/db_5.png">
<img src="https://github.com/v1a0/imgs/blob/main/sqllex/examples/1/db_6.png">


<br><br>


### Delete (drop) table

Now lest remove this new table. For this use `drop` method with name of table (`some_users`)

```python
new_table.drop()
```

<img src="https://github.com/v1a0/imgs/blob/main/sqllex/examples/1/db_1.png">
<img src="https://github.com/v1a0/imgs/blob/main/sqllex/examples/1/db_4.png">

Cool.


<br><br>


### Update data in record

As you see in table `users` first record looks not like an other. I guess we have to fix it. Just updater data of this one record.

<img src="https://github.com/v1a0/imgs/blob/main/sqllex/examples/1/db_4.png">

```python
table_users.update(
    SET=['username', 'User1'],
    WHERE=['id', 1]
)
``` 

Run it and we got:

<img src="https://github.com/v1a0/imgs/blob/main/sqllex/examples/1/db_7.png">


<br><br>


### Super!

### Congratulations you did it! Now you know how to use sqllex and admin sqlite databases!

### Explore more and learn how awesome SQL and SQLLEX is!

### [Back to home](./index.md)
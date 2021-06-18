...

users = db['users']    # Get table from database as object

id_col = users['id']    # Get table from database as object

name_col = users['name']    # Get another column from table as object


users.insert([1, 'Alex'])
users.insert([2, 'Blex'])

...

users.update(
        {
            id_col: id_col + 2
        },
        WHERE=(name_col == 'Alex')
)


users.select([name_col, id_col], WHERE=(id_col == 3))   # [['Alex', 3]]
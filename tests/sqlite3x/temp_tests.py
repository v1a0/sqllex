from sqllex import SQLite3x, INTEGER, TEXT, ALL

db = SQLite3x(path='test.db')

db.create_table(
    'users',
    {
        'id': INTEGER,
        'name': TEXT
    }
)

# Get table from database as object
users = db['users']

# Get column from table as object
urs_id = users['id']

# Get another column from table as object
usr_name = users['name']

print(users.columns_names)  # ['id', 'name']


# Inserting data
users.insert([1, 'Alex'])
users.insert([2, 'Blex'])


# SELECT * FROM users WHERE (users.id=2) OR (users.id=1)
users.select(ALL, (urs_id == 2) | (urs_id == 1))    # [[1, 'Alex'], [2, 'Blex']]


# Update name WHERE (id=1)
users.update(
    {'name': "XXXX"},
    WHERE=urs_id == 1
)


# SELECT * FROM users WHERE (users.id<>0) AND (users.id<>1)
users.select(
    [usr_name, urs_id],
    WHERE=(
        (urs_id != 0) & (urs_id != 1)
    )
)   # [['XXXX', 1], ['Blex', 2]]


# UPDATE id SET id = id + 2 WHERE (name = "XXXX")
users.update(
        {
            urs_id: urs_id + 2
        },
        WHERE=usr_name == 'XXXX'
)


a = users.select([usr_name, urs_id], WHERE=(urs_id == 3))   # [['XXXX', 3]]

print(a)
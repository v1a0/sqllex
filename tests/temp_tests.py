from sqllex import *

# Create some database, with simple structure
db = SQLite3x(                              # create database
    path='my_data.db',                      # __str__ to your database, or where_ you would like it locate
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
user = users.find(age=33)

# Print results
print(user)  # [['Sqllex', 33]]
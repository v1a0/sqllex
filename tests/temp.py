from sqllex import SQLite3x, TEXT, NOT_NULL, INTEGER

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

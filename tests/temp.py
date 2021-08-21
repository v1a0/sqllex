# import psycopg2
# from psycopg2 import Error
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
#
# connection = psycopg2.connect(
#     dbname="postgres",
#     user="postgres",
#     password="admin",
#     host="127.0.0.1",
#     port="5432"
# )
#
# cursor = connection.cursor()
# cursor.execute("""
# SELECT * FROM book
# """)
#
#
# print(cursor.fetchall())
# print(type(connection))


from sqllex import PostgreSQLx

db = PostgreSQLx(
    dbname="postgres",
    user="postgres",
    password="admin",
    host="127.0.0.1",
    port="5432"
)

print(db.select("book", '*'))
print(db.select("book", '*', WHERE=db['book']['book_id'] == 1))



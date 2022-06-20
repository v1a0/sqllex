import sqllex as sx
from datetime import datetime

db = sx.SQLite3x(':memory:', init_connection=False)

db.connect(check_same_thread=False)

db.create_table(
    'suggestions',
    {
        'sid': [sx.INTEGER, sx.PRIMARY_KEY, sx.AUTOINCREMENT],
        'uid': [sx.INTEGER, sx.NOT_NULL],
        'category': [sx.TEXT, sx.NOT_NULL],  # header|article|idea
        'status': [sx.TEXT, sx.NOT_NULL, sx.DEFAULT, "sent"],
        # sent|rejected|in_work|posted
        'comment': [sx.TEXT],
        'date': [sx.TEXT, sx.NOT_NULL]
    }, IF_NOT_EXIST=True
)

db.insert(
    'suggestions',
    {
        "uid": 1,
        "category": 'header',
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
)

print(
    db.select(
        'suggestions', sx.ALL
    )
)
# [(1, 1, 'category', 'sent', None, '2022-03-24 10:26')]

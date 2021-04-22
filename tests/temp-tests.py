from sqllex.constants.sql import CONST_PRIORITY
from sqllex.constants import *

from sqllex import *
from sqllex.types import DBTemplateType

template: DBTemplateType = {
    'users': {
        'id': [INTEGER, NOT_NULL],
    }
}

db = SQLite3x(template=template)

p = [[11], [22], [33]]

db.insertmany('users', p)

print(
db.select(
        SELECT=['username', 'group_name', 'description'],                 # SELECT username, group_name, description
        FROM=['users', AS, 'us'],                                         # FROM users AS us
        JOIN=[                                                            # JOIN
            ['groups', AS, 'gr', ON, 'us.group_id == gr.group_id'],       ## INNER JOIN groups AS gr ON us.group_id == gr.group_id
            [INNER_JOIN, 'about', 'ab', ON, 'ab.group_id == gr.group_id'] ## INNER JOIN about ab ON ab.group_id == gr.group_id
        ],
        WHERE={'username': 'user_1'},                                     # WHERE (username='user_1')
        ORDER_BY='age DESC',                                              # order by age ASC
        LIMIT=50,
        OFFSET=20,
    execute=False
    ).request.script

)


# ['INTEGER', 'REAL', 'NONE', 'AUTOINCREMENT', 'NOT NULL', 'DEFAULT', 'NULL']
# ['INTEGER', 'REAL', 'NONE', 'AUTOINCREMENT', 'NOT NULL', 'DEFAULT', 'NULL']

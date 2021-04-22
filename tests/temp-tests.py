from sqllex.constants.sql import CONST_PRIORITY
from sqllex.constants import *


def col_types_sort(val: str) -> int:
    prior = CONST_PRIORITY.get(val)

    if prior is None:
        return 1
    else:
        return prior


te = [
    PRIMARY_KEY, INTEGER, NOT_NULL
]


_te = sorted(te, key=lambda t: col_types_sort(t))

print(_te)


from sqllex import *
from sqllex.types import DBTemplateType

template: DBTemplateType = {
        'users': {
            'id': [PRIMARY_KEY, INTEGER, NOT_NULL],
        }
    }

db = SQLite3x(template=template)


# ['INTEGER', 'REAL', 'NONE', 'AUTOINCREMENT', 'NOT NULL', 'DEFAULT', 'NULL']
# ['INTEGER', 'REAL', 'NONE', 'AUTOINCREMENT', 'NOT NULL', 'DEFAULT', 'NULL']
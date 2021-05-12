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

assert 1 == 2


# ['INTEGER', 'REAL', 'NONE', 'AUTOINCREMENT', 'NOT NULL', 'DEFAULT', 'NULL']
# ['INTEGER', 'REAL', 'NONE', 'AUTOINCREMENT', 'NOT NULL', 'DEFAULT', 'NULL']

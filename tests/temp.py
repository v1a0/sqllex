from sqllex import *
from sqllex.types import *


DB_NAME = "temp_table.db"

DB_TEMPLATE: DBTemplateType = {
    "t1": {
        "text_t": TEXT,
        "num_t": NUMERIC,
        "int_t": INTEGER,
        "real_t": REAL,
        "none_t": NONE,
        "blob_t": BLOB,
    }
}

db = SQLite3x(
    path='database.db',
    init_connection=False
)

db.connect(check_same_thread=False)

print(db.tables_names)

db.disconnect()

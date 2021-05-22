from sqllex import *
from sqllex.debug import debug_mode

debug_mode(True)

db = SQLite3x('temp_test_1.db',
              template={
                  'wallets': {
                      'id': INTEGER,
                      'balance': INTEGER
                  }
              })

value = 1
user_id = 10

db.insert('wallets', 10, 5)

db.insertmany('wallets', id=[1, 2, 3], balance=[10, ])

db.update(
        TABLE='wallets',
        SET={
            'balance': f'pre_balance+{value}'
        },
        WHERE={
            'id': user_id,
        },
        WITH={
            'pre_balance': db.select(SELECT='balance',
                                     TABLE='wallets',
                                     WHERE={
                                         'id': user_id,
                                     },
                                     execute=False
                                     )
        }
    )

print(db.select_all('wallets'))

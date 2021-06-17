from numpy import array, nan
from sqllex import SQLite3x, TEXT, UNIQUE, INTEGER, REAL


data = array([['World', 2415712510, 318.1, '9.7%', nan],
              ['United States', 310645827, 949.5, '44.3%',
               'Johnson&Johnson, Moderna, Pfizer/BioNTech'],
              ['India', 252760364, 186.9, '3.5%',
               'Covaxin, Covishield, Oxford/AstraZeneca'],
              ['Brazil', 78906225, 376.7, '11.3%',
               'Oxford / AstraZeneca, Oxford/AstraZeneca, Pfizer/BioNTech, Sinovac']])

vaccine_db = SQLite3x('numpy_test.db')

vaccine_db.create_table(
    name='Total',
    columns={
        "Country": [TEXT, UNIQUE],
        "Doses_Administered": INTEGER,
        "Doses_per_1000": REAL,
        "Fully_Vaccinated_Population": TEXT,
        "Vaccine_Type_Used": TEXT
    },
    IF_NOT_EXIST=True
)

vaccine_db.updatemany('Total', data)

vaccine_db.updatemany('Total', array([[],[]]))




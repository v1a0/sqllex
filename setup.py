from setuptools import setup
from os import path
import sqllex

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sqllex',
    packages=[
        'sqllex',
        'sqllex.classes',
        'sqllex.constants',
        'sqllex.core',

        'sqllex.core.entities',
        'sqllex.core.entities.abc',
        'sqllex.core.entities.postgresqlx'
        'sqllex.core.entities.sqlite3x',

        'sqllex.core.tools',
        'sqllex.core.tools.convertors',
        'sqllex.core.tools.docs_helpers',
        'sqllex.core.tools.parsers',
        'sqllex.core.tools.sorters',

        'sqllex.debug',
        'sqllex.exceptions',
        'sqllex.old',
        'sqllex.types',
    ],
    version=sqllex.__version__,
    license='gpl-3.0',
    description='Better than sqlite3',
    author='v1a0',
    author_email='contact@v1a0.dev',
    url="https://github.com/v1a0/sqllex",
    download_url=f"https://github.com/V1A0/sqllex/archive/refs/tags/v{sqllex.__version__}.tar.gz",
    keywords=[
        'sqllex', 'sql', 'db', 'database',
        'sqlite3', 'sqlite', 'SQLite3', 'SQLite3x',
        'psycopg2', 'postgresql', 'postgres', 'psql',
        'easy', 'fast', 'orm', 'ORM',
    ],
    install_requires=[
        'loguru==0.5.3',
        'psycopg2==2.9.1',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Database',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.9',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
# https://pypi.org/classifiers/

print("""
\t\t\t\33[41m!!!\tWARNING\t!!!\033[0m
\033[91m
SQLLEX v0.2 have major changes that may breaks your old code! 
Please, read https://github.com/v1a0/sqllex/blob/main/UPDATES.md#0200
if you are moving from v0.1.10.5 to v0.2+, and open an issue if you have any bugs.
\033[0m\33[93m
Thanks for you support and feedback! \033[0m""")

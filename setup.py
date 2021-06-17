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
        'sqllex.core.entities.sqlite3x',
        'sqllex.core.entities.super',

        'sqllex.core.tools',
        'sqllex.core.tools.convertors',
        'sqllex.core.tools.parsers',
        'sqllex.core.tools.sorters',

        'sqllex.debug',
        'sqllex.exceptions',
        'sqllex.types',
    ],
    version=sqllex.__version__,
    license='gpl-3.0',
    description='Better than sqlite3',
    author='v1a0',
    author_email='None',
    url="https://github.com/v1a0/sqllex",
    download_url=f"https://github.com/V1A0/sqllex/archive/refs/tags/v{sqllex.__version__}.tar.gz",
    keywords=['sql', 'sql3', 'sqlite', 'sqlite3', 'sqllex', 'db', 'database', 'easy'],
    install_requires=[
        'colorama==0.4.4',
        'loguru==0.5.3',
        'win32-setctime==1.0.3',
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

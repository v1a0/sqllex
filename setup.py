from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sqllex',
    packages=[
        'sqllex',
        'sqllex.classes', 'sqllex.classes.sqlite3x',
        'sqllex.constants',
        'sqllex.exceptions',
        'sqllex.types',
        'sqllex.debug',
    ],
    version='0.1.9.8',
    license='gpl-3.0',
    description='Better than sqlite3',
    author='v1a0',
    url="https://github.com/v1a0/sqllex",
    download_url="https://github.com/V1A0/sqllex/archive/refs/tags/v0.1.9.8.tar.gz",
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

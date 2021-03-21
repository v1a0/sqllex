from setuptools import setup

setup(
    name='sqllex',
    packages=['sqllex', 'sqllex.classes', 'sqllex.constants', 'sqllex.exceptions', 'sqllex.types_'],
    version='0.1.1',
    license='gpl-3.0',
    description='Better than sqlite3',
    author='v1a0',
    url='https://github.com/v1a0/sqllex',
    download_url='https://github.com/V1A0/sqllex/archive/refs/tags/v0.1.1.tar.gz',
    keywords=['sql', 'sql3', 'sqlite', 'sqlite3', 'sqllex', 'db', 'database', 'easy'],
    install_requires=[  # I get to this in a second
        'colorama==0.4.4',
        'loguru==0.5.3',
        'win32-setctime==1.0.3',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',     # ????
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',  # Again, pick a license
        'Programming Language :: Python :: 3.9',
    ],
)

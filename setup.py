import os
from setuptools import setup, find_packages

setup(
    name = 'key_value_db',
	packages = ['com.azeezadewale'],
	include_package_data=True,
	version = '1.1.2',
	platforms='any',
	description = 'Quick and easy manage, load, update and save key-value type database',
	author = 'Azeez Adewale',
	author_email = 'azeezadewale98@gmail.com',
	license='LGPL-3.0',
	url = 'https://github.com/Thecarisma/key-value-db',
	zip_safe=False,
	classifiers=[
        'Development Status :: 5 - Production/Stable',
		'Natural Language :: English',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Topic :: Database',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Database :: Front-Ends',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
     ],
    keywords = [
		'key-value', 
		'database', 
		'python', 
		'package', 
		'quick', 
		'simple', 
		'dictionary'
	],
)
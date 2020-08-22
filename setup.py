import os
from setuptools import setup, find_packages

setup(
    name = 'konfiger',
	packages = ['konfiger'],
    package_dir = {
        'konfiger': 'src'
    },
	include_package_data=True,
	version = '1.2.4',
	platforms='any',
	description = 'Light weight package to manage key value based configuration and data files for Python',
    long_description = open('README.rst').read(),
	author = 'Adewale Azeez',
	author_email = 'azeezadewale98@gmail.com',
	license='MIT',
	url = 'https://konfiger.github.io/konfiger-python',
	zip_safe=False,
	classifiers=[
        'Development Status :: 5 - Production/Stable',
		'Natural Language :: English',
        #'License :: OSI Approved :: MIT License (MIT)',
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
		'thecarisma', 
		'quick', 
		'simple', 
		'dictionary'
	],
)
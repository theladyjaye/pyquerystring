#!/usr/bin/env python
import sys
import os
from setuptools import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = """Query String Parsing The Way It Should Be

Python's default urlparse.parse_qs() does not understand the concept of data structures. While this works for simple querystrings, anything more complex returns a less than desirable result.

This library is intended to inteligentally parse complex querystrings that python's library is unable to handle such as the following:

mylist[]=item0&mylist[]=item1
mylist[0]=item0&mylist[1]=item1
mylist[0][0]=subitem0&mylist[0][1]=subitem1
mylist.element=item0
mylist.element[0]=item0&mylist.element[1]=item0
"""

with open('LICENSE') as f:
    license = f.read()

packages = [
    'pyquerystring'
]

requires = []

setup(
    name='pyquerystring',
    version='1.0',
    description='Query String Parsing The Way It Should Be',
    long_description=readme,
    author='Adam Venturella',
    author_email='aventurella@gmail.com',
    url='http://github.com/aventurella/pyquerystring',
    license=license,
    packages=packages,
    package_data={'': ['LICENSE']},
    include_package_data=True,
    install_requires=requires,
    package_dir={'pyquerystring': 'pyquerystring'},
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ),

)

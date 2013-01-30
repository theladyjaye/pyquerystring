#!/usr/bin/env python
import sys
import os
from setuptools import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

packages = [
    'pyquerystring'
]

requires = []

setup(
    name='pyquerystring',
    version='0.3.0',
    description='Fancy query string parsing & application/x-www-form-urlencoded parsing',
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
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
    ),

)

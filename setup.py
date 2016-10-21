import os
from setuptools import setup

setup(
    name = 'logipy',
    version = '1.2.1',
    author = 'Tom Lambert',
    author_email = 'devtechsupport@logitech.com',
    description = ('A simple python wrapper for Logitech G\'s LED and Arx SDKs.'),
    long_description = open('README.rst').read(),
    keywords = ['logi', 'logipy', 'Logitech', 'LogitechG', 'LED', 'Arx', 'LGS', 'Logitech Gaming Software'],
    url = 'http://gaming.logitech.com/en-us/developers',
	download_url = 'https://github.com/Logitech/logiPy/tarball/master',
    packages=['logipy'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Libraries',
    ],
    license='MIT',
)
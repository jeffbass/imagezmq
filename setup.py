""""
Simple copy-paste from setup.py of
https://github.com/jakubroztocil/httpie
:)
I'm too lazy to do it from scratch!
"""
# This is purely the result of trial and error.
#

import sys
import codecs

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import imagezmq

###TODO write some tests, for example two processes that send some pics over TCP etc.

# class PyTest(TestCommand):
#     # `$ python setup.py test' simply installs minimal requirements
#     # and runs the tests with no fancy stuff like parallel execution.
#     def finalize_options(self):
#         TestCommand.finalize_options(self)
#         self.test_args = [
#             '--doctest-modules', '--verbose',
#             './httpie', './tests'
#         ]
#         self.test_suite = True
#
#     def run_tests(self):
#         import pytest
#         sys.exit(pytest.main(self.test_args))
#
#
# tests_require = [
#     # Pytest needs to come last.
#     # https://bitbucket.org/pypa/setuptools/issue/196/
#     'pytest-httpbin',
#     'pytest',
#     'mock',
# ]


install_requires = [
    'imutils~=0.5',
    'pyzmq>=0.16',
    'opencv-python~=4.1'
]


# Conditional dependencies:

# sdist
if 'bdist_wheel' not in sys.argv:
    try:
        # noinspection PyUnresolvedReferences
        import argparse
    except ImportError:
        install_requires.append('argparse>=1.2.1')

    if 'win32' in str(sys.platform).lower():
        # Terminal colors for Windows
        install_requires.append('colorama>=0.2.4')


# bdist_wheel
extras_require = {
    # https://wheel.readthedocs.io/en/latest/#defining-conditional-dependencies
    'python_version == "3.0" or python_version == "3.1"': ['argparse>=1.2.1'],
    ':sys_platform == "win32"': ['colorama>=0.2.4'],
    'python_version == "3.5" or python_version == "3.6" or python_version == "3.7" or python_version == "3.8"': ['numpy~=1.7'],
}


def long_description():
    with codecs.open('README.rst', encoding='utf8') as f:
        return f.read()


setup(
    name='imagezmq',
    version=imagezmq.__version__,
    description=imagezmq.__doc__.strip(),
    long_description=long_description(),
    url='https://www.yin-yang-ranch.com/',
    download_url='https://github.com/WeLikeCode/imagezmq',
    author=imagezmq.__author__,
    author_email='jeff@yin-yang-ranch.com',
    license=imagezmq.__license__,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'http = imagezmq.__main__:main',
            'https = imagezmq.__main__:main',
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    #tests_require=tests_require,
    #cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 0.1 - Development/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        #'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development',
        'Topic :: System :: Networking',
        'Topic :: Terminals',
        'Topic :: Image Processing',
        'Topic :: Utilities'
    ],
)
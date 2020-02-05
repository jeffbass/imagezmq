# Based on setup.py (for humans):
#     https://github.com/navdeep-G/setup.py
#     and from: https://github.com/psf/requests/blob/master/setup.py
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

packages = ['imagezmq']

requires = [
    'pyzmq>=16.0',
    'numpy>=1.13',
]

about = {}
with open(os.path.join(here, 'imagezmq', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

with open('PyPI_README.rst', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/x-rst',
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=packages,
    package_dir={'imagezmq': 'imagezmq'},
    python_requires=">=3.5",
    install_requires=requires,
    license=about['__license__'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License'
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    project_urls={
        'Documentation': 'https://requests.readthedocs.io',
        'Source': 'https://github.com/psf/requests',
    },
)

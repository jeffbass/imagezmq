# Version History and Changelog

All notable changes the **imageZMQ** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Development

- Adding and testing `close()` method in `ImageSender` and `ImageHub` classes.
- Adding and testing `__enter__` and `__exit__` methods.
- Adding keywords variable to setup.py to improve PyPI repository.
- Adding history variable to setup.py.

## 1.0.2 - 2020-05-12

### Improvements

- Added Advanced PUB/SUB example with multithreaded fast subscribers for realtime processing.
 (@philipp-schmidt).
- Added this HISTORY.md file to document project changes.
- Fixed inconsistent spellings of `imageZMQ`.

### Changes and Bugfixes

- Multiple fixes to all documentation files.
- Fixed documentation of API, adding `connect()` method to ImageHub class docs.

## 1.0.1 - 2020-02-11

### Improvements

- Added setup.py, MANIFEST.in and PyPI_README.rst to enable pip installation and upload to PyPI.
- Added new images /docs/image/various_badges.svg with static badge images to improve README.rst load time.
- Reference as 1st Release in GitHub, PyPI (2020-02-05) and Zendodo (2020-02-12).

### Changes and Bugfixes

- Changed README.rst to show badges referenced in badge_fetch.rst.
- Changed README.rst to include pip install instructions.
- Multiple fixes to all documentation files.

## 0.0.3 - 2019-08-23

### Improvements

- Implementation of PUB/SUB ZMQ messaging pattern (@bigdaddymax).
- Example of PUB/SUB ZMQ messaging pattern (@bigdaddymax).
- Example of HTTP Steaming Example (@bigdaddymax).
- Helpful fork: Add timeouts to `ImageSender` to fix restarts or non-response of `ImageHub` timeouts (@youngsoul).

### Changes and Bugfixes

- Multiple fixes to all documentation files.
- Substantial rewrite of API, to include and clean up PUB/SUB option docs.

## 0.0.2 - 2019-02-09

### Improvements

- More detail and uniform formatting for docstrings and code snippets in docs.
- Additional tests and test docs.

### Changes and Bugfixes

- Multiple fixes to all documentation files.
- Restructured test files & testing documentation to make them consistent.

## 0.0.1 - 2018-03-03

- First Commit of `imageZMQ` prototype to GitHub on Mar 3, 2018.

## 0.0.0 - 2016-01-09

- First early prototype of `imageZMQ` posted as a GitHub Gist on Jan 9, 2016.
- Gist is [here](https://gist.github.com/jeffbass/ebf877e964c9a0b84272).

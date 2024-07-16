# Version History and Changelog

All notable changes the **imageZMQ** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Ongoing Development

- Testing **imageZMQ** with newer versions of Python (through 3.11)
- Modifying tests to use Picamera2 and latest Raspberry Pi OS

- Improving documentation content, layout, arrangement.
- Including additional Example programs and documentation.
- Adding more questions to FAQs doc file.

## 1.1.1 - 2020-05-22

### Improvements

- Added `__enter__` and `__exit__` methods so that `ImageHub` and
  `ImageSender` will work in a `with` statement.
- Added history and keywords to setup.py.

### Changes and Bugfixes

- Multiple fixes to documentation files.

## 1.1.0 - 2020-05-20

### Improvements

- Added `tests/unit_tests` directory to hold "tests of new imageZMQ features".
  Also added README_Unit_Tests.rst in that directory to explain Unit Tests for
  imageZMQ improvements going forward.
- Added `close()` method in `ImageSender` and `ImageHub` classes. Added 2 test
  programs to `tests/unit_tests` to test it. Added `close()` to API docs.
- Added Advanced PUB/SUB example with multithreaded fast subscribers for
  realtime processing. (@philipp-schmidt).
- Added this `HISTORY.md` file to document version change history.
- Fixed inconsistent spellings of `imageZMQ`.

### Changes and Bugfixes

- Multiple fixes to documentation files.
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

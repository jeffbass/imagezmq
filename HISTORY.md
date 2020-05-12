# Version History and Changelog

All notable changes the **imageZMQ** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Development

- Adding and testing `close()` method in `ImageSender` and `ImageHub` classes
- Adding and testing `__enter__` and `__exit__` methods

## 1.0.2 - 2020-05-12

### Added

- Advanced PUB/SUB example with multithreaded fast subscribers for realtime processing.
 (@philipp-schmidt).
- This HISTORY.md file to document project changes.

### Changed

- Multiple changes to all documentation files.

## 1.0.1 - 2020-02-11

### Added

- setup.py, MANIFEST.in and PyPI_README.rst to enable pip installation and upload to PyPI.
- New images /docs/image/various_badges.svg with static badge images to improve README.rst load time.
- Reference as 1st Release in GitHub.

### Changed

- Changed README.rst to show badges referenced in badge_fetch.rst.
- Changed README.rst to include pip install instructions.

## 0.0.3 - 2019-08-23

### Added

- Implementation of PUB/SUB ZMQ messaging pattern (@bigdaddymax).
- Example of PUB/SUB ZMQ messaging pattern (@bigdaddymax).
- Example of HTTP Steaming Example (@bigdaddymax).
- Helpful fork: Add timeouts to `ImageSender` to fix restarts or non-response of `ImageHub` timeouts (@youngsoul).

### Changed

- Multiple changes to all documentation files.

## 0.0.2 - 2019-02-09

### Added

- More detail and uniform formatting for docstrings and code snippets in docs.

### Changed
- Multiple changes to all documentation files.

## 0.0.1 - 2018-03-03

- First Commit of `imageZMQ` prototype to GitHub on Mar 3, 2018.

## 0.0.0 - 2016-01-09

- First early prototype posted as a GitHub Gist on Jan 9, 2016
- Gist is [here](https://gist.github.com/jeffbass/ebf877e964c9a0b84272).

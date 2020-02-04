# copied from setup.py (for humans):
#     https://github.com/navdeep-G/setup.py

# This small x_setup.py file is for testing small bits of setup code

import io
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))

# this code snippet tests that we can:
# Load the package's __version__.py module as a dictionary.
about = {}
with open(os.path.join(here, 'imagezmq', '__version__.py')) as f:
    exec(f.read(), about)
print(about)

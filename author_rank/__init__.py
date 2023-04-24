"""

AuthorRank
========

AuthorRank is a Python package that implements a modification of PageRank to
find the most prestigious authors in a scientific collaboration network.

See https://github.com/adidier17/AuthorRank.
"""

import sys
if sys.version_info[:2] < (3, 5):
    m = "Python 3.5 or later is required for AuthorRank (%d.%d detected)."
    raise ImportError(m % sys.version_info[:2])
del sys

__author__ = "Valentino Constantinou, Annie Didier"
__version__ = "0.1.3"

import author_rank.graph
from author_rank.graph import *

import author_rank.score
from author_rank.score import *

import author_rank.utils
from author_rank.utils import *


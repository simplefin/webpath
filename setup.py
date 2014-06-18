# Copyright (c) The SimpleFIN Team
# See LICENSE for details.

from setuptools import setup
from pip.req import parse_requirements

import re
import os

def getVersion():
    """
    Get version from version file without importing.
    """
    r = re.compile(r'__version__ = "(.*?)"')
    version_file = os.path.join(os.path.dirname(__file__), 'webpath/version.py')
    fh = open(version_file, 'rb')
    for line in fh.readlines():
        m = r.match(line)
        if m:
            return m.groups()[0]

def getRequirements():
    reqs = []
    for req in parse_requirements('requirements.txt'):
        reqs.append(str(req.req))
    return reqs



setup(
    url='https://github.com/simplefin/webpath',
    author='Matt Haggard',
    author_email='matt@simplefin.org',
    name='webpath',
    version=getVersion(),
    packages=[
        'webpath', 'webpath.test',
    ],
    scripts=[
        'bin/webpath',
    ],
    install_requires=getRequirements(),
)

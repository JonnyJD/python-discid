#!/usr/bin/env python

from distutils.core import setup
from discid import _version

setup(name="discid",
        version=_version,
        description="Python binding of Libdiscid",
        long_description=open("README.md").read(),
        author="Johannes Dewender",
        author_email="brainz@JonnyJD.net",
        url="https://github.com/JonnyJD/python-discid",
        license="LGPLv3+",
        py_modules = ["discid"],
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Ripping",
            "Topic :: Software Development :: Libraries :: Python Modules"
            ]
        )

# vim:set shiftwidth=4 smarttab expandtab:

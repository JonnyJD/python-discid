#!/usr/bin/env python

import sys
import unittest
from distutils.core import setup, Command
from discid import _VERSION


class Test(Command):
    description = "run the test suite"
    # options as listed with "--help test"
    # --verbose --quiet -> self.verbose are already handles as global options
    user_options = [
            ("tests=", None,
                "a comma separated list of tests to run (default all)")
            ]

    def initialize_options(self):
        # set defaults
        self.tests = None

    def finalize_options(self):
        if self.verbose:
            self.verbosity = 2
        else:
            self.verbosity = 1
        if self.tests is not None:
            if self.tests:
                self.names = self.tests.split(",")
            else:
                self.names = []
        else:
            self.names = ["test_discid"]

    def run(self):
        suite = unittest.defaultTestLoader.loadTestsFromNames(self.names)
        runner = unittest.TextTestRunner(verbosity=self.verbosity)
        result = runner.run(suite)
        if result.wasSuccessful():
            sys.exit(0)
        else:
            sys.exit(len(result.failures) + len(result.errors))


setup(name="discid",
        version=_VERSION,
        description="Python binding of Libdiscid",
        long_description=open("README.rst").read(),
        author="Johannes Dewender",
        author_email="brainz@JonnyJD.net",
        url="https://python-discid.readthedocs.org/",
        license="LGPLv3+",
        py_modules = ["discid"],
        cmdclass = {"test": Test},
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

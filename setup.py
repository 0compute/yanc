#!/usr/bin/env python

import os

from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()

# under test we do not want the nose entry point installed because it screws up
# coverage since the package is imported too early
if "YANC_NO_NOSE" in os.environ:
    entry_points = None
else:
    entry_points = {
        "nose.plugins": ("yanc=yanc.yancplugin:YancPlugin",),
        }

setup(name="yanc",
      version="0.2.3",
      description="Yet another nose colorer",
      long_description=README,
      license="MIT",
      keywords="nose color",
      author="Arthur Noel",
      author_email="arthur@0compute.net",
      url="https://github.com/0compute/yanc",
      packages=("yanc",),
      entry_points=entry_points,
      )

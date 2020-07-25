#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='import_media',
      version='0.0.1dev',
      description='Python utilities to import and organize media',
      url='http://github.com/asundaresan/import_media',
      author='Aravind Sundaresan',
      author_email='asundaresan@gmail.com',
      license='GPLv3',
      packages=find_packages(),
      scripts=[
        "bin/import_photos.py",
        ],
      zip_safe=False,
      install_requires = [
          "exifread"
        ]
      )


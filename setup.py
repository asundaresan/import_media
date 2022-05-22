#!/usr/bin/env python

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read()

setup(name='import_media',
      version='0.0.1dev',
      description='Python utilities to import and organize media files, specifically photos.',
      url='http://github.com/asundaresan/import_media',
      author='Aravind Sundaresan',
      author_email='asundaresan@gmail.com',
      license='GPLv3',
      packages=find_packages(),
      #package_data={
      #    'import_data': [
      #        'data/*/*.h5', 
      #        ]
      #    },
      #scripts=[
      #  "bin/import_files.py",
      #  "bin/get_metadata.py",
      #  ],
      zip_safe=False,
      install_requires = requirements,
      entry_points={
          'console_scripts': [
              'import_files=import_media.import_files:main',
              ],
          },
      )


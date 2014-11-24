from setuptools import setup, find_packages
import sys, os

version = '1.0.0'

install_requires = [
    # -*- Extra requirements: -*-
    ]

setup(name='Minesweeper',
      version=version,
      description="Tool to analyse the sentiment of youtube comments in Python",
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Development Status :: 1 - Planning",
          "Environment :: Console",
          "Intended Audience :: Education",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          ],
      keywords='youtube, sentiment, comments',
      author='A. Castro, J. Okkels, R. Gutke',
      author_email='s141272@student.dtu.dk',
      url='https://github.com/MiningPythonGroup/Minesweeper',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=install_requires,
      )
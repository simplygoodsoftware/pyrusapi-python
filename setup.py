import os
from setuptools import setup, find_packages

setup(name="pyrus-api",
      version="1.28.0",
      python_requires='>=3.4',
      description="Python Pyrus API client",
      author="Pyrus",
      long_description=open('README.rst', 'r').read(),
      author_email="contact@pyrus.com",
      url="https://pyrus.com/en/help/api",
      packages=find_packages(exclude=["*tests.*", "*test.*"]),
      keywords="pyrus api",
      install_requires=[
          'requests',
          'jsonpickle',
          'rfc6266'
      ],
      zip_safe=True)

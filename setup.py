import os

from setuptools import setup
from setuptools.command.build_py import build_py
from libbash import configure_bash

class build_libbash(build_py):
    def run(self):
        build_py.run(self)
        configure_bash()
        os.system("git submodule update --init --recursive")



setup(name='libbash',
      packages=['libbash'],
      cmdclass={'build_py': build_libbash},
      version='0.1.0',
      description="A Python library for parsing Bash scripts into an AST",
      url="https://github.com/binpash/libbash/",
      author='Seth Sabar',
      author_email='sethsabar@gmail.com',
      license="GPL-3.0",
      include_package_data=True,
      has_ext_modules=lambda: True)

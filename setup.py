import os
import sys
import subprocess

from setuptools import setup
from setuptools.command.build_py import build_py


def try_exec(*cmds):
    proc = subprocess.run(cmds)

    if proc.returncode != 0:
        print('`{}` failed'.format(' '.join(cmds)), file=sys.stderr)
        proc.check_returncode()

class build_libbash(build_py):
    def run(self):
        build_py.run(self)
        try_exec('cd', 'libbash/bash-5.2', '&&', './configure', '&&', 'make', 'clean', 'all')

setup(name='libbash',
      packages=['libbash', 'libbash.bash_command'],
      cmdclass={'build_py': build_libbash},
      package_data={'libbash': ['bash-5.2/*']},
      version='0.1.2',
      description="A Python library for parsing Bash scripts into an AST",
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      url="https://github.com/binpash/libbash/",
      author='Seth Sabar',
      author_email='sethsabar@gmail.com',
      license="GPL-3.0",
      include_package_data=True,
      has_ext_modules=lambda: True)


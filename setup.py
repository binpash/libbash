import os
import sys
import subprocess
import shutil

from setuptools import setup
from setuptools.command.build_py import build_py
from contextlib import ContextDecorator



def try_exec(*cmds):
    proc = subprocess.run(cmds)

    if proc.returncode != 0:
        print('`{}` failed'.format(' '.join(cmds)), file=sys.stderr)
        proc.check_returncode()

class enter_dir(ContextDecorator):
    def __init__(self, path):
        self.path = path
        self.old_path = os.getcwd()
    def __enter__(self):
        os.chdir(self.path)
        return self

    def __exit__(self, *exc):
        os.chdir(self.old_path)
        return False

class build_libbash(build_py):
    def run(self):
        build_py.run(self)

        with enter_dir('libbash/bash-5.2'):
            try_exec('./configure')
            try_exec('make', 'clean', 'all')


setup(name='libbash',
      packages=['libbash', 'libbash.bash_command'],
      cmdclass={'build_py': build_libbash},
      package_data={'libbash': ['bash-5.2/*']},
      version='0.1.4',
      description="A Python library for parsing Bash scripts into an AST",
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      url="https://github.com/binpash/libbash/",
      author='Seth Sabar',
      author_email='sethsabar@gmail.com',
      license="GPL-3.0",
      include_package_data=True,
      has_ext_modules=lambda: True)


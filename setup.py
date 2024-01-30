import os

from setuptools import setup
from setuptools.command.build_py import build_py


class build_libbash(build_py):
    def run(self):
        build_py.run(self)
        os.system("git submodule update --init --recursive")
        os.system("cd " + os.path.join
                  (os.path.dirname(__file__), "libbash", "bash-5.2") +
                  " && ./configure && make clean all")

setup(name='libbash',
      packages=['libbash', 'libbash.bash_command'],
      cmdclass={'build_py': build_libbash},
      version='0.1.0',
      description="A Python library for parsing Bash scripts into an AST",
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      url="https://github.com/binpash/libbash/",
      author='Seth Sabar',
      author_email='sethsabar@gmail.com',
      license="GPL-3.0",
      include_package_data=True,
      has_ext_modules=lambda: True)


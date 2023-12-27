from .common import BASH_FILE_PATH
import os


def configure_bash() -> None:
    """
    Runs the configure script and compiles bash.
    """
    os.system("cd " + os.path.dirname(BASH_FILE_PATH) +
              " && ./configure && make clean all")

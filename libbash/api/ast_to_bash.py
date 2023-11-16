from ..bash_command import *
from .api_common import _setup_bash
import ctypes


def ast_to_bash(ast: list[Command], reconfigure: bool = False) -> str:
    """
    Converts the AST of a bash script back into the bash source code.
    :param ast: The AST of the bash script
    :param reconfigure: If true, the configure script and make clean all
    will be called before parsing the bash file. By default this is set to false, but
    if the bash source hasn't been compiled yet, this flag will be ignored.
    :return: The bash source code
    """
    bash = _setup_bash(reconfigure)

    # specify arg types and return type of make_command_string function
    bash.make_command_string.argtypes = [ctypes.POINTER(c_bash.command)]
    bash.make_command_string.restype = ctypes.c_char_p

    bash_str = ""

    for command in ast:
        command_string = bash.make_command_string(command._to_ctypes())
        bash_str += command_string.decode('utf-8')
        bash_str += "\n"

    return bash_str

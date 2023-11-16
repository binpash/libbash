from ..c_bash import ctypes_bash_command as c_bash
from ..bash_command import Command
from .common import _setup_bash
import ctypes
import os

# current location + ../../bash-5.2/bash.so
BASH_FILE_PATH = os.path.join(os.path.dirname(
    __file__), "..", "..", "bash-5.2", "bash.so")


def bash_to_ast(bash_file: str, reconfigure: bool = False) -> list[Command]:
    """
    Extracts the AST from the bash source code.
    Uses ctypes to call an injected bash function that returns the AST.

    :param bash_file: The path to the bash file to parse
    :param reconfigure: If true, the configure script and make clean all
    will be called before parsing the bash file. By default this is set to false, but
    if the bash source hasn't been compiled yet, this flag will be ignored.
    """

    bash = _setup_bash(reconfigure)

    # tell python arg types and return type of the set_bash_file function
    bash.set_bash_file.argtypes = [ctypes.c_char_p]
    bash.set_bash_file.restype = ctypes.c_int

    # call the function
    set_result: ctypes.c_int = bash.set_bash_file(bash_file.encode('utf-8'))
    if set_result < 0:
        raise Exception("Bash file set failed")

    # tell python arg types and return type of the read_command_safe function
    bash.read_command_safe.argtypes = []
    bash.read_command_safe.restype = ctypes.c_int

    command_list: list[Command] = []

    while True:
        # call the function
        read_result: ctypes.c_int = bash.read_command_safe()
        if read_result != 0:
            raise Exception(
                "Bash read command failed, shell script may be invalid")

        # read the global_command variable
        global_command: ctypes.POINTER(c_bash.command) = ctypes.POINTER(
            c_bash.command).in_dll(bash, 'global_command')

        # global_command is null
        if not global_command:
            eof_reached: ctypes.c_int = ctypes.c_int.in_dll(
                bash, 'EOF_Reached')
            if eof_reached:
                break
            else:
                # newline probably
                continue

        # read the command
        command = Command(global_command.contents)

        # add the command to the list
        command_list.append(command)

    return command_list

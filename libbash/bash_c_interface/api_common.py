import ctypes
import os

# current location + ../../bash-5.2/bash.so
BASH_FILE_PATH = os.path.join(os.path.dirname(
    __file__), "..", "..", "bash-5.2", "bash.so")


def _setup_bash(reconfigure: bool) -> ctypes.CDLL:
    if reconfigure or not os.path.isfile(BASH_FILE_PATH):
        # run configure and make clean all
        # this will compile the bash source code into a shared object file
        # that can be called from python using ctypes
        os.system("cd " + os.path.dirname(BASH_FILE_PATH) +
                  " && ./configure && make clean all")

    if not os.path.isfile(BASH_FILE_PATH):
        raise Exception("Bash file not found at path: " + BASH_FILE_PATH)

    try:
        bash = ctypes.CDLL(BASH_FILE_PATH)
    except OSError:
        raise Exception(
            "Bash shared object file not found at path: " + BASH_FILE_PATH)

    # tell python arg types and return type of the initialize_shell_libbash
    bash.initialize_shell_libbash.argtypes = []
    bash.initialize_shell_libbash.restype = ctypes.c_int

    # call the function
    init_result: ctypes.c_int = bash.initialize_shell_libbash()
    if init_result != 0:
        raise Exception("Bash initialization failed")

    return bash

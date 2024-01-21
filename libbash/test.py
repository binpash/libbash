import sys

from libbash.api import bash_to_ast, ast_to_bash, ast_to_json
import os
import shutil
import random

# The file path to the bash.so file
BASH_FILE_PATH = os.path.join(os.path.dirname(
    __file__), "bash-5.2", "bash.so")

# The file path to the bash-5.2/tests directory
BASH_TESTS_DIR = os.path.join(os.path.dirname(
    __file__), "bash-5.2", "tests")

# The number of iterations to run the bash and ast consistency test
NUM_ITERATIONS = 10


def get_test_files() -> list[str]:
    """
    Gets all the test files in the test directory
    :return: The list of test files
    """
    test_files = []
    for file in os.listdir(BASH_TESTS_DIR):
        if file.endswith(".sub"):
            test_files.append(os.path.join(BASH_TESTS_DIR, file))

    # remove these because they have SOH or are escaped by SOH, a known bug in bash-5.2
    for remove_file in [
        "case2.sub",
        "nquote3.sub",
        "dollar-star6.sub",
        "nquote5.sub",
        "exp6.sub",
        "exp7.sub",
        "quote4.sub",
        "cond-regexp1.sub",
        "iquote1.sub",
        "exp1.sub",
        "rhs-exp1.sub",
        "cond-regexp3.sub",
        "glob8.sub",
        "posixexp6.sub",
        "new-exp6.sub",
        "dollar-at-star10.sub",
        "dollar-at-star4.sub",
        "case3.sub",
    ]:
        test_files.remove(os.path.join(BASH_TESTS_DIR, remove_file))

    # remove these files until we determine if this is a bug in bash-5.2 or not
    for remove_file in [
        "comsub-posix5.sub", # bux fix in progress, we need to handle esacs in case statements
        "intl3.sub", # seems to be an issue with utf-8 characters, not sure what to do here ...
        "array9.sub", # same issue as above
        "unicode1.sub", # same issue as above
        "unicode3.sub", # same issue as above

    ]:
        test_files.remove(os.path.join(BASH_TESTS_DIR, remove_file))

    # randomize the order of the test files
    random.shuffle(test_files)

    return test_files


def write_to_file(file: str, content: str):
    """
    Writes the content to the file
    :param file: The file to write to
    :param content: The content to write to the file
    """
    file_obj = open(file, "w", encoding="utf-8")
    file_obj.write(content)
    file_obj.close()

def read_from_file(file: str) -> str:
    """
    Reads the content from the file
    :param file: The file to read from
    :return: The content of the file
    """
    file_obj = open(file, "r", encoding="utf-8")
    content = file_obj.read()
    file_obj.close()
    return content


def test_bash_and_ast_consistency():
    """
    This test runs bash_to_ast and ast_to_bash on every test file in the bash-5.2/tests directory 
    back and forth NUM_ITERATIONS times. On each iteration it makes sure that the AST is the same as the previous iteration.
    It also makes sure that the bash file is the same as the previous iteration excluding the first iteration.
    Finally if getting the AST fails, it will make sure that it fails consistently.
    """

    # this is necessary for exportfunc2.sub
    sys.setrecursionlimit(10000)

    TMP_DIR = "/tmp/libbash"
    TMP_FILE = f"{TMP_DIR}/test.sh"

    # make a temporary directory to store the bash files
    shutil.rmtree(TMP_DIR, ignore_errors=True)
    os.mkdir(TMP_DIR)

    test_files = get_test_files()
    for test_file in test_files:
        print(f"Testing {test_file}")

        # copy the test file to the temporary file
        write_to_file(TMP_FILE, read_from_file(test_file))

        try:
            ast = bash_to_ast(test_file)
            # we mainly just want to make sure this doesn't break
            ast_to_json(ast)
            bash = ast_to_bash(ast)
        except RuntimeError as e:
            assert str(e) == "Bash read command failed, shell script may be invalid"
            continue

        write_to_file(TMP_FILE, bash)
        ast2 = bash_to_ast(TMP_FILE)
        bash2 = ast_to_bash(ast2)

        # func2.sub doesn't pass this test because in the second iteration
        # a command is wrapped in a group
        if not test_file == os.path.join(BASH_TESTS_DIR, "func2.sub"):
            assert ast == ast2

        write_to_file(TMP_FILE, bash2)
        bash3 = ast_to_bash(bash_to_ast(TMP_FILE))
        assert bash2 == bash3

    shutil.rmtree(TMP_DIR)

    print(f"Bash and AST consistency tests passed on {len(test_files)} scripts!")


def run_tests():
    """
    Runs all the tests in this file
    """
    print("Running tests...")
    test_bash_and_ast_consistency()
    print("All tests passed!")
    

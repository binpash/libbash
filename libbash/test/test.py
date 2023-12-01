from ..api import bash_to_ast, ast_to_bash, ast_to_json
import os

BASH_FILE_PATH = os.path.join(os.path.dirname(
    __file__), "..", "..", "bash-5.2", "bash.so")

BASH_TESTS_DIR = os.path.join(os.path.dirname(
    __file__), "..", "..", "bash-5.2", "tests")


def get_test_files() -> list[str]:
    """
    Gets all the test files in the test directory
    :return: The list of test files
    """
    test_files = []
    for file in os.listdir(BASH_TESTS_DIR):
        if file.endswith(".sub"):
            test_files.append(os.path.join(BASH_TESTS_DIR, file))
    return test_files


def test_bash_to_ast_equality():
    """
    This test runs bash_to_ast on every test file in the bash-5.2/tests directory and
    captures the output. Then, it converts the ast back into bash source code via
    ast_to_bash and the back via bash_to_ast. The resulting AST is compared to the
    original AST and if they are not equal, the test fails.
    """
    TMP_DIR = "/tmp/libbash"
    TMP_FILE = "/tmp/libbash/test.sh"

    # make a temporary directory to store the bash files
    os.system(f"rm -rf {TMP_DIR}")
    os.system(f"mkdir {TMP_DIR}")
    for test_file in get_test_files():
        try:
            ast = bash_to_ast(test_file)
            print(test_file)
        except Exception as e:
            continue
        bash = ast_to_bash(ast)
        os.system(f"echo '{bash}' > {TMP_FILE}")
        ast2 = bash_to_ast(f"{TMP_FILE}")
        os.system(f"rm {TMP_FILE}")
        assert ast == ast2

    os.system(f"rm -rf {TMP_DIR}")


def run_tests():
    """
    Runs all the tests in this file
    """
    print("Running tests...")
    test_bash_to_ast_equality()
    print("bash_to_ast equality test passed!")
    print("All tests passed!")
    

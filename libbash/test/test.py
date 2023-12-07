from ..api import bash_to_ast, ast_to_bash, ast_to_json
import os
import shutil

BASH_FILE_PATH = os.path.join(os.path.dirname(
    __file__), "..", "..", "bash-5.2", "bash.so")

BASH_TESTS_DIR = os.path.join(os.path.dirname(
    __file__), "..", "..", "bash-5.2", "tests")

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
    TMP_DIR = "/tmp/libbash"
    TMP_FILE = f"{TMP_DIR}/test.sh"

    # make a temporary directory to store the bash files
    shutil.rmtree(TMP_DIR)
    os.mkdir(TMP_DIR)

    for test_file in get_test_files():
        print(f"Testing {test_file}")

        # copy the test file to the temporary file
        write_to_file(TMP_FILE, read_from_file(test_file))

        valid_script = True
        try:
            ast = bash_to_ast(test_file)
            bash = ast_to_bash(ast)
        except Exception as e:
            valid_script = False
        
        for i in range(NUM_ITERATIONS):
            if not valid_script:
                try:
                    ast = bash_to_ast(test_file)
                    print("ERROR: bash script parsing is inconsistently failing")
                    assert False
                except Exception as e:
                    continue

            write_to_file(TMP_FILE, bash)
            ast2 = bash_to_ast(TMP_FILE)
            bash2 = ast_to_bash(ast2)
            
            assert ast == ast2
            if i != 0:
                assert bash == bash2
            
            ast = ast2
            bash = bash2

    shutil.rmtree(TMP_DIR)


def run_tests():
    """
    Runs all the tests in this file
    """
    print("Running tests...")
    test_bash_and_ast_consistency()
    print("bash_and_ast_consistency test passed!")
    print("All tests passed!")
    

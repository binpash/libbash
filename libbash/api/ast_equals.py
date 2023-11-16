from ..bash_command import *


def ast_equals(ast1: list[Command], ast2: list[Command]) -> bool:
    """
    Checks if two ASTs are equal. Note that this function does not consider 
    style differences, such as line numbers, spacing, etc.
    :param ast1: The first AST
    :param ast2: The second AST
    :return: True if the ASTs are equal, False otherwise
    """
    if len(ast1) != len(ast2):
        return False

    for i in range(len(ast1)):
        if ast1[i] != ast2[i]:
            return False

    return True

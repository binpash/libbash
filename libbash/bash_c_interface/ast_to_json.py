from libbash import Command


def ast_to_json(ast: list[Command]) -> list[dict[str, any]]:
    """
    Converts the AST to a JSON style object.
    :param ast: The AST, a list of Command objects.
    :return: A JSON style object, a list of dicts from str to JSON style object.
    """
    return [command._to_json() for command in ast]

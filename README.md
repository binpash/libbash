# libbash

## API

`bash_to_ast` takes as input a file containing a bash script and optionally a boolean indicating whether the bash-5.2 source executable doing the parsing should be re-made (by default this is false). It returns a `list` of `Command`s (see AST Classes below) representing the AST of the script. This function will throw an Exception if the script is invalid.

`ast_to_json` takes as input a `list` of `Command`s and returns a list of json-style object's representing the `Command`s (we say that a json-style object is either a `map` from `str` to json-style object or a `str`, `int`, `null`, or `list` of json-style object).

## Command Objects

This library represents the AST of bash scripts with Python classes. These classes closely mirror structs in the bash-5.2 source code. Below is an explanation of each of these classes.

Coming soon ...

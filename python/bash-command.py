from enum import Enum
from typing import Union, Optional
from json import JSONEncoder


class WordDesc:
    word: str
    flags: int

    def to_json(self) -> dict[str, Union(int, str)]:
        return {
            'word': self.word,
            'flags': self.flags
        }


class RedirecteeUnion:
    # use only if R_DUPLICATING_INPUT or R_DUPLICATING_OUTPUT
    dest: Optional[int]
    # use otherwise
    word: Optional[WordDesc]

    def to_json(self) -> dict[str, Union(int, str, dict, list)]:
        if self.dest is not None:
            return {
                'dest': self.dest
            }
        elif self.word is not None:
            return {
                'word': self.word.to_json()
            }
        else:
            raise Exception('invalid redirectee')

    def validate(self):
        assert sum([1 if x is not None else 0 for x in [
                   self.dest, self.word]]) == 1


class CommandType(Enum):
    """
    a command type enum
    """
    CM_FOR = 0  # for loop
    CM_CASE = 1  # switch case
    CM_WHILE = 2  # while loop
    CM_IF = 3  # if statement
    CM_SELECT = 4  # select statement
    CM_SIMPLE = 5  # simple command
    CM_CONNECTION = 6  # probably connectors like &,||, &&, ;
    CM_FUNCTION_DEF = 7  # function definition
    CM_UNTIL = 8  # until loop
    CM_GROUP = 9  # probably a command grouping via { } or ( )
    CM_ARITH = 10  # arithmetic expression, probably using $(( ))
    CM_COND = 11  # conditional expression, probably using [[ ]]
    CM_ARITH_FOR = 12  # probably for loop using (( ))
    CM_SUBSHELL = 13  # subshell via ( )
    CM_COPROC = 14  # coprocess


class RInstruction(Enum):
    """
    a redirection instruction enum
    """
    R_OUTPUT_DIRECTION = 0  # >foo
    R_INPUT_DIRECTION = 1  # <foo
    R_INPUTA_DIRECTION = 2  # foo & makes this
    R_APPENDING_TO = 3  # >>foo
    R_READING_UNTIL = 4  # << foo
    R_READING_STRING = 5  # <<< foo
    R_DUPLICATING_INPUT = 6  # 1<&2
    R_DUPLICATING_OUTPUT = 7  # 1>&2
    R_DEBLANK_READING_UNTIL = 8  # <<-foo
    R_CLOSE_THIS = 9  # <&-
    R_ERR_AND_OUT = 10  # command &>filename
    R_INPUT_OUTPUT = 11  # <>foo
    R_OUTPUT_FORCE = 12  # >| foo
    R_DUPLICATING_INPUT_WORD = 13  # 1<&$foo
    R_DUPLICATING_OUTPUT_WORD = 14  # 1>&$foo
    R_MOVE_INPUT = 15  # 1<&2-
    R_MOVE_OUTPUT = 16  # 1>&2-
    R_MOVE_INPUT_WORD = 17  # 1<&$foo-
    R_MOVE_OUTPUT_WORD = 18  # 1>&$foo-
    R_APPEND_ERR_AND_OUT = 19  # &>> filename

    # converts redirection type actual bash redirection string
    def to_json(self) -> str:
        if self == RInstruction.R_OUTPUT_DIRECTION:
            return '>'
        elif self == RInstruction.R_INPUT_DIRECTION:
            return '<'
        elif self == RInstruction.R_INPUTA_DIRECTION:
            return '&'  # ?
        elif self == RInstruction.R_APPENDING_TO:
            return '>>'
        elif self == RInstruction.R_READING_UNTIL:
            return '<<'
        elif self == RInstruction.R_READING_STRING:
            return '<<<'
        elif self == RInstruction.R_DUPLICATING_INPUT:
            return '<&'
        elif self == RInstruction.R_DUPLICATING_OUTPUT:
            return '>&'
        elif self == RInstruction.R_DEBLANK_READING_UNTIL:
            return '<<-'
        elif self == RInstruction.R_CLOSE_THIS:
            return '<&-'
        elif self == RInstruction.R_ERR_AND_OUT:
            return '&>'
        elif self == RInstruction.R_INPUT_OUTPUT:
            return '<>'
        elif self == RInstruction.R_OUTPUT_FORCE:
            return '>|'
        elif self == RInstruction.R_DUPLICATING_INPUT_WORD:
            return '<&$'  # todo figure out if $ is needed
        elif self == RInstruction.R_DUPLICATING_OUTPUT_WORD:
            return '>&$'  # todo figure out if $ is needed
        elif self == RInstruction.R_MOVE_INPUT:
            return '<&-'
        elif self == RInstruction.R_MOVE_OUTPUT:
            return '>&-'
        elif self == RInstruction.R_MOVE_INPUT_WORD:
            return '<&$-'  # todo figure out if $ is needed
        elif self == RInstruction.R_MOVE_OUTPUT_WORD:
            return '>&$-'  # todo figure out if $ is needed
        elif self == RInstruction.R_APPEND_ERR_AND_OUT:
            return '&>>'
        else:
            raise Exception('invalid redirect instruction')


class CondTypeEnum(Enum):
    """
    a conditional expression type enum
    """
    COND_AND = 0
    COND_OR = 1
    COND_UNARY = 2
    COND_BINARY = 3
    COND_TERM = 4
    COND_EXPR = 5


class Redirect:
    """
    describes a redirection such as >, >>, <, <<
    """
    redirector: RedirecteeUnion  # the thing being redirected
    rflags: int  # not sure what this is
    flags: int  # flag value for open?
    instruction: RInstruction  # the type of redirection
    redirectee: RedirecteeUnion  # the thing being redirected to
    here_doc_eof: str  # the word that appeared in the << operator?

    def to_json(self) -> dict[str, Union(int, str, dict, list)]:
        return {
            'redirector': self.redirector.to_json(),
            'rflags': self.rflags,
            'flags': self.flags,
            'instruction': self.instruction.name,
            'redirectee': self.redirectee.to_json(),
            'here_doc_eof': self.here_doc_eof
        }


class ForCom:
    """
    a for command class
    """
    flags: int  # command flags
    line: int  # line number the command is on?
    name: WordDesc  # the variable name to get mapped over?
    map_list: list[WordDesc]  # the list of words to map over
    action: list['Command']  # the action to take for each word in the map list


class Pattern:
    """
    represents a pattern in a case command
    """
    patterns: list[WordDesc]  # the list of patterns to match against
    action: 'Command'  # the action to take if the pattern matches
    flags: int  # not sure what flag type this is


class CaseCom:
    """
    a case command class
    """
    flags: int  # command flags
    line: int  # line number the command is on?
    word: WordDesc  # the thing to match against
    clauses: list[Pattern]  # the list of patterns to match against


class WhileCom:
    """
    a while command class
    """
    flags: int  # command flags
    test: 'Command'  # the thing to test
    action: 'Command'  # the action to take while the test is true


class IfCom:
    """
    an if command class
    """
    flags: int  # command flags
    test: 'Command'  # the thing to test
    true_case: 'Command'  # the action to take if the test is true
    false_case: Optional['Command']  # the action to take if the test is false


class Connection:
    """
    represents connections
    """
    ignore: int  # unused but keep for consistency
    first: 'Command'  # the first command to run
    second: 'Command'  # the second command to run
    connector: int  # the connector to use?


class SimpleCom:
    """
    a simple command class
    """
    flags: int  # command flags
    line: int  # line number the command is on
    words: list[WordDesc]  # program name, arguments, variable assignments, etc
    redirects: list[Redirect]  # redirections


class FunctionDef:
    """
    for function definitions
    """
    flags: int  # command flags
    line: int  # line number the command is on
    name: WordDesc  # the name of the function
    command: 'Command'  # the execution tree for the function
    source_file: Optional[str]  # the file the function was defined in, if any


class GroupCom:
    """
    group commands allow pipes and redirections to be applied to a group of commands
    """
    ignore: int  # is this used?
    command: 'Command'  # the command to run


class SelectCom:
    """
    the select command is like a for loop but with a menu
    """
    flags: int  # command flags
    line: int  # line number the command is on
    name: WordDesc  # the name of the variable?
    map_list: list[WordDesc]  # the list of words to map over
    action: 'Command'  # the action to take for each word in the map list, during execution name is bound to member of map_list


class ArithCom:
    """
    arithmetic expression ((...))
    """
    flags: int  # not sure what flag type this is
    line: int  # line number the command is on
    exp: WordDesc  # the expression to evaluate


class CondCom:
    """
    conditional expression [[...]]
    """
    flags: int  # unclear flag type
    line: int  # line number the command is on
    type: CondTypeEnum  # the type of conditional expression
    op: WordDesc  # unclear
    left: Optional['Command']  # the left side of the expression
    right: Optional['Command']  # the right side of the expression


class ArithForCom:
    """
    a c-style for loop ((init; test; step)) action
    """
    flags: int  # unclear flag type
    line: int  # line number the command is on
    init: list[WordDesc]  # the initial values of the variables
    test: list[WordDesc]  # the test to perform
    step: list[WordDesc]  # the step to take
    action: 'Command'  # the action to take for each iteration


class SubshellCom:
    """
    a subshell command
    """
    flags: int  # unclear flag type
    line: int  # line number the command is on
    command: 'Command'  # the command to run in the subshell

    def to_json(self) -> dict[str, Union(int, str, dict, list)]:
        return {
            'type': 'subshell',
            'flags': self.flags,
            'line': self.line,
            'command': self.command.to_json()
        }


class CoprocCom:
    """
    a coprocess command
    """
    flags: int  # unclear flag type
    name: WordDesc  # the name of the coprocess
    command: 'Command'  # the command to run in the coprocess

    def to_json(self) -> dict[str, Union(int, str, dict, list)]:
        return {
            'type': 'coproc',
            'flags': self.flags,
            'name': self.name.to_json(),
            'command': self.command.to_json()
        }


class ValueUnion:
    """
    a union of all the possible command types
    exactly one of these will be non-null
    """
    for_com: Optional[ForCom]
    case_com: Optional[CaseCom]
    while_com: Optional[WhileCom]
    if_com: Optional[IfCom]
    connection: Optional[Connection]
    simple_com: Optional[SimpleCom]
    function_def: Optional[FunctionDef]
    group_com: Optional[GroupCom]
    select_com: Optional[SelectCom]
    arith_com: Optional[ArithCom]
    cond_com: Optional[CondCom]
    arith_for_com: Optional[ArithForCom]
    subshell_com: Optional[SubshellCom]
    coproc_com: Optional[CoprocCom]

    def validate(self):
        assert sum(
            [
                1 if x is not None else 0
                for x in [
                    self.for_com,
                    self.case_com,
                    self.while_com,
                    self.if_com,
                    self.connection,
                    self.simple_com,
                    self.function_def,
                    self.group_com,
                    self.select_com,
                    self.arith_com,
                    self.cond_com,
                    self.arith_for_com,
                    self.subshell_com,
                    self.coproc_com,
                ]
            ]
        ) == 1


class Command:
    """
    a mirror of the bash command struct defined here:
    https://git.savannah.gnu.org/cgit/bash.git/tree/command.h
    """
    type: CommandType  # command type
    flags: int  # not sure what this is
    line: int  # line number the command is on
    redirects: list[Redirect]
    value: ValueUnion

    def validate(self):
        assert self.value.validate()
        for redirect in self.redirects:
            assert redirect.redirector.validate()
            assert redirect.redirectee.validate()

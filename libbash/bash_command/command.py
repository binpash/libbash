from enum import Enum
from typing import Union, Optional
from ..bash_c_interface import ctypes_bash_command as c_bash
import ctypes
from .flags import *


class WordDesc:
    word: str
    flags: list[WordDescFlag]

    def __init__(self, word: c_bash.word_desc):
        """
        :param word: the word description
        """
        self.word = word.word.decode('utf-8')
        self.flags = word_desc_flag_list_from_int(word.flags)

    def _to_json(self) -> dict[str, Union[int, str]]:
        """
        :return: a dictionary representation of the word description
        """
        return {
            'word': self.word,
            'flags': [x._to_json() for x in self.flags]
        }


def word_desc_list_from_word_list(word_list: ctypes.POINTER(c_bash.word_list)) -> list[WordDesc]:
    """
    :param word: the word list
    :return: a list of word descriptions
    """
    word_desc_list = []
    while word_list:
        word_desc_list.append(WordDesc(word_list.contents.word.contents))
        word_list = word_list.contents.next
    return word_desc_list


class RedirecteeUnion:
    # use only if R_DUPLICATING_INPUT or R_DUPLICATING_OUTPUT
    dest: Optional[int]
    # use otherwise
    filename: Optional[WordDesc]

    def __init__(self, dest: Optional[int], filename: Optional[c_bash.word_desc]):
        """
        :param dest: the destination file descriptor or None
        :param word: the word description or None
        """
        self.dest = dest if dest is not None else None
        self.filename = WordDesc(filename) if filename else None

    def _to_json(self) -> dict[str, Union[int, str, dict, list]]:
        """
        :return: a dictionary representation of the redirectee union
        """
        if self.dest is not None:
            return {
                'dest': self.dest
            }
        elif self.filename is not None:
            return {
                'filename': self.filename._to_json()
            }
        else:
            raise Exception('invalid redirectee')


class Redirect:
    """
    describes a redirection such as >, >>, <, <<
    """
    redirector: RedirecteeUnion  # the thing being redirected
    rflags: list[RedirectFlag]  # flags for redirection
    flags: list[OFlag]
    instruction: RInstruction  # the type of redirection
    redirectee: RedirecteeUnion  # the thing being redirected to
    here_doc_eof: Optional[str]  # the word that appeared in the << operator?

    def __init__(self, redirect: c_bash.redirect):
        """
        :param redirect: the redirect struct
        """
        self.rflags = redirect_flag_list_from_rflags(redirect.rflags)
        self.flags = oflag_list_from_int(redirect.flags)
        self.instruction = RInstruction(redirect.instruction)
        self.here_doc_eof = redirect.here_doc_eof.decode(
            'utf-8') if redirect.here_doc_eof is not None else None
        if RedirectFlag.REDIR_VARASSIGN in self.rflags:
            self.redirector = RedirecteeUnion(
                None, redirect.redirector.filename.contents)
        else:
            self.redirector = RedirecteeUnion(redirect.redirector.dest, None)
        if self.instruction == RInstruction.R_DUPLICATING_INPUT or \
                self.instruction == RInstruction.R_DUPLICATING_OUTPUT or \
                self.instruction == RInstruction.R_CLOSE_THIS or \
                self.instruction == RInstruction.R_MOVE_INPUT or \
                self.instruction == RInstruction.R_MOVE_OUTPUT:
            self.redirectee = RedirecteeUnion(redirect.redirectee.dest, None)
        else:
            self.redirectee = RedirecteeUnion(
                None, redirect.redirectee.filename.contents)

    def _to_json(self) -> dict[str, Union[int, str, dict, list]]:
        """
        :return: a dictionary representation of the redirect struct
        """
        return {
            'redirector': self.redirector._to_json(),
            'rflags': [x._to_json() for x in self.rflags],
            'flags': [x._to_json() for x in self.flags],
            'instruction': self.instruction._to_json(),
            'redirectee': self.redirectee._to_json(),
            'here_doc_eof': self.here_doc_eof if self.here_doc_eof is not None else None
        }


def redirect_list_from_redirect(redirect: ctypes.POINTER(c_bash.redirect)) -> list[Redirect]:
    redirect_list = []
    while redirect:
        redirect_list.append(Redirect(redirect.contents))
        redirect = redirect.contents.next
    return redirect_list


class ForCom:
    """
    a for command class
    """
    flags: list[CommandFlag]
    line: int  # line number the command is on?
    name: WordDesc  # the variable name to get mapped over?
    map_list: list[WordDesc]  # the list of words to map over
    action: 'Command'  # the action to take for each word in the map list

    def __init__(self, for_c: c_bash.for_com):
        self.flags = command_flag_list_from_int(for_c.flags)
        self.line = for_c.line
        self.name = WordDesc(for_c.name.contents)
        self.map_list = word_desc_list_from_word_list(for_c.map_list)
        self.action = Command(for_c.action.contents)

    def _to_json(self) -> dict[str, Union[int, str, dict, list]]:
        return {
            'flags': self.flags,
            'line': self.line,
            'name': self.name._to_json(),
            'map_list': [x._to_json() for x in self.map_list],
            'action': self.action._to_json()
        }


class Pattern:
    """
    represents a pattern in a case command
    """
    patterns: list[WordDesc]  # the list of patterns to match against
    action: 'Command'  # the action to take if the pattern matches
    flags: list[PatternFlag]

    def __init__(self, pattern: c_bash.pattern_list):
        self.patterns = word_desc_list_from_word_list(pattern.patterns)
        self.action = Command(pattern.action.contents)
        self.flags = pattern_flag_list_from_int(pattern.flags)

    def _to_json(self) -> dict[str, Union[int, dict, list]]:
        return {
            'patterns': [x._to_json() for x in self.patterns],
            'action': self.action._to_json(),
            'flags': self.flags
        }


def pattern_list_from_pattern_list(pattern: ctypes.POINTER(c_bash.pattern_list)) -> list[Pattern]:
    pattern_list = []
    while pattern is not None:
        pattern_list.append(Pattern(pattern.contents))
        pattern = pattern.contents.next
    return pattern_list


class CaseCom:
    """
    a case command class
    """
    flags: list[CommandFlag]
    line: int  # line number the command is on?
    word: WordDesc  # the thing to match against
    clauses: list[Pattern]  # the list of patterns to match against

    def __init__(self, case_c: c_bash.case_com):
        self.flags = command_flag_list_from_int(case_c.flags)
        self.line = case_c.line
        self.word = WordDesc(case_c.word.contents)
        self.clauses = pattern_list_from_pattern_list(case_c.clauses)

    def _to_json(self) -> dict[str, Union[int, str, dict, list]]:
        return {
            'flags': self.flags,
            'line': self.line,
            'word': self.word._to_json(),
            'clauses': [x._to_json() for x in self.clauses]
        }


class WhileCom:
    """
    a while command class
    """
    flags: list[CommandFlag]
    test: 'Command'  # the thing to test
    action: 'Command'  # the action to take while the test is true

    def __init__(self, while_c: c_bash.while_com):
        self.flags = command_flag_list_from_int(while_c.flags)
        self.test = Command(while_c.test.contents)
        self.action = Command(while_c.action.contents)

    def _to_json(self) -> dict[str, Union[int, str, dict]]:
        return {
            'flags': self.flags,
            'test': self.test._to_json(),
            'action': self.action._to_json()
        }


class IfCom:
    """
    an if command class
    """
    flags: list[CommandFlag]
    test: 'Command'  # the thing to test
    true_case: 'Command'  # the action to take if the test is true
    false_case: Optional['Command']  # the action to take if the test is false

    def __init__(self, if_c: c_bash.if_com):
        self.flags = command_flag_list_from_int(if_c.flags)
        self.test = Command(if_c.test.contents)
        self.true_case = Command(if_c.true_case.contents)
        self.false_case = Command(
            if_c.false_case.contents) if if_c.false_case else None

    def _to_json(self) -> dict[str, Union[int, str, dict]]:
        return {
            'flags': self.flags,
            'test': self.test._to_json(),
            'true_case': self.true_case._to_json(),
            'false_case': self.false_case._to_json() if self.false_case is not None else None
        }


class Connection:
    """
    represents connections
    """
    ignore: list[CommandFlag]
    first: 'Command'  # the first command to run
    second: Optional['Command']  # the second command to run
    connector: ConnectionType  # the type of connection

    def __init__(self, connection: c_bash.connection):
        self.ignore = command_flag_list_from_int(connection.ignore)
        self.first = Command(connection.first.contents)
        self.second = Command(
            connection.second.contents) if connection.second else None
        self.connector = ConnectionType(connection.connector)

    def _to_json(self) -> dict[str, Union[int, str, dict]]:
        return {
            'ignore': [x._to_json() for x in self.ignore],
            'first': self.first._to_json(),
            'second': self.second._to_json() if self.second is not None else None,
            'connector': self.connector._to_json()  # todo: figure out what this int means
        }


class SimpleCom:
    """
    a simple command class
    """
    flags: list[CommandFlag]
    line: int  # line number the command is on
    words: list[WordDesc]  # program name, arguments, variable assignments, etc
    redirects: list[Redirect]  # redirections

    def __init__(self, simple: c_bash.simple_com):
        self.flags = command_flag_list_from_int(simple.flags)
        self.line = simple.line
        self.words = word_desc_list_from_word_list(simple.words)
        self.redirects = redirect_list_from_redirect(simple.redirects)

    def _to_json(self) -> dict[str, Union[int, str, dict, list]]:
        return {
            'flags': [x._to_json() for x in self.flags],
            'line': self.line,
            'words': [x._to_json() for x in self.words],
            'redirects': [x._to_json() for x in self.redirects]
        }


class FunctionDef:
    """
    for function definitions
    """
    flags: list[CommandFlag]
    line: int  # line number the command is on
    name: WordDesc  # the name of the function
    command: 'Command'  # the execution tree for the function
    source_file: Optional[str]  # the file the function was defined in, if any

    def __init__(self, function: c_bash.function_def):
        self.flags = command_flag_list_from_int(function.flags)
        self.line = function.line
        self.name = WordDesc(function.name.contents)
        self.command = Command(function.command.contents)
        self.source_file = function.source_file if function.source_file is not None else None

    def _to_json(self) -> dict[str, Union[int, str, dict, None]]:
        return {
            'flags': [x._to_json() for x in self.flags],
            'line': self.line,
            'name': self.name._to_json(),
            'command': self.command._to_json(),
            'source_file': self.source_file if self.source_file is not None else None
        }


class GroupCom:
    """
    group commands allow pipes and redirections to be applied to a group of commands
    """
    ignore: list[CommandFlag]
    command: 'Command'  # the command to run

    def __init__(self, group: c_bash.group_com):
        self.ignore = command_flag_list_from_int(group.ignore)
        self.command = Command(group.command.contents)

    def _to_json(self) -> dict[str, Union[int, str, dict]]:
        return {
            'ignore': [x._to_json() for x in self.ignore],
            'command': self.command._to_json()
        }


class SelectCom:
    """
    the select command is like a for loop but with a menu
    """
    flags: list[CommandFlag]
    line: int  # line number the command is on
    name: WordDesc  # the name of the variable?
    map_list: list[WordDesc]  # the list of words to map over
    action: 'Command'  # the action to take for each word in the map list, during execution name is bound to member of map_list

    def __init__(self, select: c_bash.select_com):
        self.flags = command_flag_list_from_int(select.flags)
        self.line = select.line
        self.name = WordDesc(select.name)
        self.map_list = word_desc_list_from_word_list(select.map_list)
        self.action = Command(select.action.contents)

    def _to_json(self) -> dict[str, Union[int, str, dict, list]]:
        return {
            'flags': [x._to_json() for x in self.flags],
            'line': self.line,
            'name': self.name._to_json(),
            'map_list': [x._to_json() for x in self.map_list],
            'action': self.action._to_json()
        }


class ArithCom:
    """
    arithmetic expression ((...))
    """
    flags: list[CommandFlag]
    line: int  # line number the command is on
    exp: list[WordDesc]  # the expression to evaluate

    def __init__(self, arith: c_bash.arith_com):
        self.flags = command_flag_list_from_int(arith.flags)
        self.line = arith.line
        self.exp = word_desc_list_from_word_list(arith.exp)

    def _to_json(self) -> dict[str, Union[int, str, dict]]:
        return {
            'flags': [x._to_json() for x in self.flags],
            'line': self.line,
            'exp': [x._to_json() for x in self.exp]
        }


class CondCom:
    """
    conditional expression [[...]]
    """
    flags: list[CommandFlag]
    line: int  # line number the command is on
    type: CondTypeEnum  # the type of conditional expression
    op: WordDesc  # binary tree vibe?
    left: Optional['CondCom']  # the left side of the expression
    right: Optional['CondCom']  # the right side of the expression

    def __init__(self, cond: c_bash.cond_com):
        self.flags = command_flag_list_from_int(cond.flags)
        self.line = cond.line
        self.type = CondTypeEnum(cond.type)
        self.op = WordDesc(cond.op.contents)
        self.left = CondCom(
            cond.left.contents) if cond.left else None
        self.right = CondCom(
            cond.right.contents) if cond.right else None

    def _to_json(self) -> dict[str, Union[int, str, dict]]:
        return {
            'flags': [x._to_json() for x in self.flags],
            'line': self.line,
            'cond_type': self.type._to_json(),
            'op': self.op._to_json(),
            'left': self.left._to_json() if self.left is not None else None,
            'right': self.right._to_json() if self.right is not None else None
        }


class ArithForCom:
    """
    a c-style for loop ((init; test; step)) action
    """
    flags: list[CommandFlag]
    line: int  # line number the command is on
    init: list[WordDesc]  # the initial values of the variables
    test: list[WordDesc]  # the test to perform
    step: list[WordDesc]  # the step to take
    action: 'Command'  # the action to take for each iteration

    def __init__(self, arith_for: c_bash.arith_for_com):
        self.flags = command_flag_list_from_int(arith_for.flags)
        self.line = arith_for.line
        self.init = word_desc_list_from_word_list(arith_for.init)
        self.test = word_desc_list_from_word_list(arith_for.test)
        self.step = word_desc_list_from_word_list(arith_for.step)
        self.action = Command(arith_for.action.contents)

    def _to_json(self) -> dict[str, Union[int, str, dict, list]]:
        return {
            'flags': [x._to_json() for x in self.flags],
            'line': self.line,
            'init': [x._to_json() for x in self.init],
            'test': [x._to_json() for x in self.test],
            'step': [x._to_json() for x in self.step],
            'action': self.action._to_json()
        }


class SubshellCom:
    """
    a subshell command
    """
    flags: list[CommandFlag]  # unclear flag type
    line: int  # line number the command is on
    command: 'Command'  # the command to run in the subshell

    def __init__(self, subshell: c_bash.subshell_com):
        self.flags = command_flag_list_from_int(subshell.flags)
        self.line = subshell.line
        self.command = Command(subshell.command.contents)

    def _to_json(self) -> dict[str, Union[int, str, dict]]:
        return {
            'flags': [x._to_json() for x in self.flags],
            'line': self.line,
            'command': self.command._to_json()
        }


class CoprocCom:
    """
    a coprocess command
    """
    flags: list[CommandFlag]  # unclear flag type
    name: str  # the name of the coprocess
    command: 'Command'  # the command to run in the coprocess

    def __init__(self, coproc: c_bash.coproc_com):
        self.flags = command_flag_list_from_int(coproc.flags)
        # c_char_p is a bytes object so we need to decode it
        self.name = coproc.name.decode('utf-8')
        self.command = Command(coproc.command.contents)

    def _to_json(self) -> dict[str, Union[int, str, dict]]:
        return {
            'flags': [x._to_json() for x in self.flags],
            'name': self.name,
            'command': self.command._to_json()
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

    def __init__(
            self,
            command_type: CommandType,
            value: c_bash.value):
        self.for_com = None
        self.case_com = None
        self.while_com = None
        self.if_com = None
        self.connection = None
        self.simple_com = None
        self.function_def = None
        self.group_com = None
        self.select_com = None
        self.arith_com = None
        self.cond_com = None
        self.arith_for_com = None
        self.subshell_com = None
        self.coproc_com = None

        if command_type == CommandType.CM_FOR:
            self.for_com = ForCom(value.For.contents)
        elif command_type == CommandType.CM_CASE:
            self.case_com = CaseCom(value.Case.contents)
        elif command_type == CommandType.CM_WHILE:
            self.while_com = WhileCom(value.While.contents)
        elif command_type == CommandType.CM_IF:
            self.if_com = IfCom(value.If.contents)
        elif command_type == CommandType.CM_CONNECTION:
            self.connection = Connection(value.Connection.contents)
        elif command_type == CommandType.CM_SIMPLE:
            self.simple_com = SimpleCom(value.Simple.contents)
        elif command_type == CommandType.CM_FUNCTION_DEF:
            self.function_def = FunctionDef(value.Function_def.contents)
        elif command_type == CommandType.CM_GROUP:
            self.group_com = GroupCom(value.Group.contents)
        elif command_type == CommandType.CM_SELECT:
            self.select_com = SelectCom(value.Select.contents)
        elif command_type == CommandType.CM_ARITH:
            self.arith_com = ArithCom(value.Arith.contents)
        elif command_type == CommandType.CM_COND:
            self.cond_com = CondCom(value.Cond.contents)
        elif command_type == CommandType.CM_ARITH_FOR:
            self.arith_for_com = ArithForCom(value.ArithFor.contents)
        elif command_type == CommandType.CM_SUBSHELL:
            self.subshell_com = SubshellCom(value.Subshell.contents)
        elif command_type == CommandType.CM_COPROC:
            self.coproc_com = CoprocCom(value.Coproc.contents)
        else:
            raise Exception('Unknown command type provided.')

    def _to_json(self) -> dict[str, dict]:
        if self.for_com is not None:
            return self.for_com._to_json()
        elif self.case_com is not None:
            return self.case_com._to_json()
        elif self.while_com is not None:
            return self.while_com._to_json()
        elif self.if_com is not None:
            return self.if_com._to_json()
        elif self.connection is not None:
            return self.connection._to_json()
        elif self.simple_com is not None:
            return self.simple_com._to_json()
        elif self.function_def is not None:
            return self.function_def._to_json()
        elif self.group_com is not None:
            return self.group_com._to_json()
        elif self.select_com is not None:
            return self.select_com._to_json()
        elif self.arith_com is not None:
            return self.arith_com._to_json()
        elif self.cond_com is not None:
            return self.cond_com._to_json()
        elif self.arith_for_com is not None:
            return self.arith_for_com._to_json()
        elif self.subshell_com is not None:
            return self.subshell_com._to_json()
        elif self.coproc_com is not None:
            return self.coproc_com._to_json()
        else:
            raise Exception('invalid value union')


class Command:
    """
    a mirror of the bash command struct defined here:
    https://git.savannah.gnu.org/cgit/bash.git/tree/command.h
    """
    type: CommandType  # command type
    flags: list[CommandFlag]  # command flags
    # line: int  # line number the command is on - seems to be unused
    redirects: list[Redirect]
    value: ValueUnion

    def __init__(self, bash_command: c_bash.command):
        self.type = CommandType(bash_command.type)
        self.flags = command_flag_list_from_int(bash_command.flags)
        # self.line = bash_command.line
        self.redirects = redirect_list_from_redirect(bash_command.redirects)
        self.value = ValueUnion(self.type, bash_command.value)

    def _to_json(self) -> dict[str, Union[int, str, dict, list]]:
        return {
            'type': self.type._to_json(),
            'flags': self.flags,
            # 'line': self.line,
            'redirects': [x._to_json() for x in self.redirects],
            'value': self.value._to_json()
        }
